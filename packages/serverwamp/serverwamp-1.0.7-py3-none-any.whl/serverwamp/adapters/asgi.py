from abc import ABCMeta
from http.cookies import CookieError, SimpleCookie
from typing import AsyncIterator, Awaitable, Callable, Mapping, Union

import msgpack

from serverwamp.connection import Connection
from serverwamp.helpers import objects_from_msgpack_batch, pack_uint32_be
from serverwamp.json import JSON_BATCH_SPLITTER
from serverwamp.json import deserialize as deserialize_json
from serverwamp.json import jsons_from_batch
from serverwamp.json import serialize as serialize_json

# In order of preference.
SUPPORTED_WS_PROTOCOLS = (
    'wamp.2.msgpack.batched',
    'wamp.2.msgpack',
    'wamp.2.json.batched',
    'wamp.2.json',
)

supported_subset = frozenset(SUPPORTED_WS_PROTOCOLS).intersection
protocol_preference = SUPPORTED_WS_PROTOCOLS.index


def scope_cookies(scope: Mapping):
    for header_name, header_value in scope['headers']:
        if header_name.upper() == 'COOKIE':
            try:
                cookie = SimpleCookie(header_value)
            except CookieError:
                return None
            break
    else:
        return {}

    return {key: morsel.value for key, morsel in cookie.items()}


async def handle_asgi_path_not_found(
    scope: Mapping,
    receive: Callable[[], Awaitable[Mapping]],
    send: Callable[[Mapping], Awaitable]
):
    if scope['type'] == 'websocket':
        await send({'type': 'websocket.close'})
        return

    await send({
        'type': 'http.response.start',
        'status': 404,
    })
    await send({'type': 'http.response.body'})


async def connection_for_asgi_invocation(
    scope: Mapping,
    receive: Callable[[], Awaitable[Mapping]],
    send: Callable[[Mapping], Awaitable]
):
    if scope['type'] != 'websocket':
        await send({
            'type': 'http.response.start',
            'status': 426,
        })
        await send({
            'type': 'http.response.body',
            'body': b'WebSocket upgrade required.'
        })
        return None

    client_subprotocols = supported_subset(scope['subprotocols'])
    if client_subprotocols:
        subprotocol = sorted(
            client_subprotocols,
            key=protocol_preference
        )[0]
    else:
        subprotocol = SUPPORTED_WS_PROTOCOLS[0]

    await send({
        'type': 'websocket.accept',
        'subprotocol': subprotocol
    })
    cookies = scope_cookies(scope)
    construct_connection = ws_protocol_connection_classes[subprotocol]
    connection = construct_connection(
        scope,
        receive,
        send,
        cookies
    )
    return connection


class ASGIWebSocketConection(Connection, metaclass=ABCMeta):
    def __init__(self, asgi_scope, asgi_receiver, asgi_sender, cookies):
        super().__init__()
        self._asgi_scope = asgi_scope
        self._asgi_receive = asgi_receiver
        self._asgi_send = asgi_sender
        self.transport_info['http_cookies'] = cookies
        self.transport_info['http_headers_raw'] = asgi_scope['headers']

    async def iterate_ws_msgs(
        self,
        data_type: str
    ) -> AsyncIterator[Union[bytes, str]]:
        """Get all WebSocket messages of a certain type. Close connection
        if wrong type comes through (WAMP WebSockets don't mix types)
        """
        while True:
            recvd = await self._asgi_receive()
            if recvd['type'] == 'websocket.receive':
                if data_type not in recvd:
                    await self.abort('wamp.error.protocol_error')
                    break
                yield recvd[data_type]
                continue
            if recvd['type'] == 'websocket.disconnect':
                break

    async def close(self):
        await self._asgi_send({'type': 'websocket.close'})


class ASGIJSONWebSocketConnection(ASGIWebSocketConection):
    async def iterate_msgs(self):
        async for ws_msg in self.iterate_ws_msgs('text'):
            yield deserialize_json(ws_msg)

    async def send_msg(self, msg):
        await self._asgi_send({
            'type': 'websocket.send',
            'text': deserialize_json(msg)
        })


class ASGIBatchedJSONWebSocketConnection(ASGIWebSocketConection):
    async def iterate_msgs(self):
        async for ws_msg in self.iterate_ws_msgs('text'):
            for msg in jsons_from_batch(ws_msg):
                yield msg

    async def send_msg(self, msg):
        await self._asgi_send({
            'type': 'websocket.send',
            'text': serialize_json(msg) + JSON_BATCH_SPLITTER
        })

    async def send_msgs(self, msgs):
        await self._asgi_send({
            'type': 'websocket.send',
            'text': JSON_BATCH_SPLITTER.join(
                    [serialize_json(msg) for msg in msgs]
                ) + JSON_BATCH_SPLITTER
        })


class ASGIMsgPackWebSocketConnection(ASGIWebSocketConection):
    async def iterate_msgs(self):
        async for ws_msg in self.iterate_ws_msgs('bytes'):
            yield msgpack.unpackb(ws_msg, use_list=False)

    async def send_msg(self, msg):
        msg_bytes = msgpack.packb(msg)
        await self._asgi_send({
            'type': 'websocket.send',
            'bytes': msg_bytes
        })


class ASGIBatchedMsgPackWebSocketConnection(ASGIWebSocketConection):
    async def iterate_msgs(self):
        async for ws_msg in self.iterate_ws_msgs('bytes'):
            for msg in objects_from_msgpack_batch(ws_msg):
                yield msg

    async def send_msg(self, msg):
        msg_bytes = msgpack.packb(msg)
        msg_len_bytes = pack_uint32_be(len(msg_bytes))
        await self._asgi_send({
            'type': 'websocket.send',
            'bytes': msg_len_bytes + msg_bytes
        })

    async def send_msgs(self, msgs):
        batch_bytes = bytearray()
        for msg in msgs:
            msg_bytes = msgpack.packb(msg)
            msg_len_bytes = pack_uint32_be(len(msg_bytes))
            batch_bytes += msg_len_bytes
            batch_bytes += msg_bytes
        await self._asgi_send({
            'type': 'websocket.send',
            'bytes': batch_bytes
        })


ws_protocol_connection_classes = {
    'wamp.2.msgpack': ASGIMsgPackWebSocketConnection,
    'wamp.2.msgpack.batched': ASGIBatchedMsgPackWebSocketConnection,
    'wamp.2.json': ASGIJSONWebSocketConnection,
    'wamp.2.json.batched': ASGIBatchedJSONWebSocketConnection
}
