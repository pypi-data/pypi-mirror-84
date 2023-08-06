from abc import ABCMeta
from ssl import SSLObject
from typing import Optional

import aiohttp
import msgpack
from aiohttp import WSMsgType, web

from serverwamp.connection import Connection
from serverwamp.helpers import objects_from_msgpack_batch, pack_uint32_be
from serverwamp.json import JSON_BATCH_SPLITTER
from serverwamp.json import deserialize as deserialize_json
from serverwamp.json import jsons_from_batch
from serverwamp.json import serialize as serialize_json

SUPPORTED_WS_PROTOCOLS = (
    'wamp.2.msgpack',
    'wamp.2.msgpack.batched',
    'wamp.2.json',
    'wamp.2.json.batched',
)


async def connection_for_aiohttp_request(request: aiohttp.web.Request):
    ws = web.WebSocketResponse(protocols=SUPPORTED_WS_PROTOCOLS)
    await ws.prepare(request)

    construct_connection = ws_protocol_connection_classes[ws.ws_protocol]
    connection = construct_connection(ws, request)
    return connection


class AiohttpWebSocketConnection(Connection, metaclass=ABCMeta):
    def __init__(
        self,
        ws: aiohttp.web.WebSocketResponse,
        request: aiohttp.web.Request,
        compress_outbound=False
    ):
        super().__init__()
        self._compress_outbound = compress_outbound
        self._ws = ws

        self.transport_info['http_cookies'] = request.cookies
        self.transport_info['http_headers_raw'] = request.raw_headers
        self.transport_info['http_path'] = request.path
        self.transport_info['http_path_raw'] = request.raw_path
        self.transport_info['http_query_string'] = request.query_string
        self.transport_info['peer_address'] = request.remote
        if request.transport:
            self.transport_info['peer_certificate'] = (
                request.transport.get_extra_info('peercert')
            )
            ssl_obj: Optional[SSLObject] = (
                request.transport.get_extra_info('ssl_object')
            )
            if ssl_obj:
                self.transport_info['peer_certificate_raw'] = (
                    ssl_obj.getpeercert(binary_form=True)
                )

    async def close(self):
        await self._ws.close()


class AiohttpJSONWebSocketConnection(AiohttpWebSocketConnection):
    async def iterate_msgs(self):
        async for ws_msg in self._ws:
            if ws_msg.type == WSMsgType.TEXT:
                yield deserialize_json(ws_msg.data)

    async def send_msg(self, msg):
        await self._ws.send_json(
            msg,
            compress=self._compress_outbound
        )


class AiohttpBatchedJSONWebSocketConnection(AiohttpWebSocketConnection):
    async def iterate_msgs(self):
        async for ws_msg in self._ws:
            if ws_msg.type == WSMsgType.TEXT:
                for msg in jsons_from_batch(ws_msg.data):
                    yield msg

    async def send_msg(self, msg):
        await self._ws.send_str(
            serialize_json(msg) + JSON_BATCH_SPLITTER,
            compress=self._compress_outbound
        )

    async def send_msgs(self, msgs):
        await self._ws.send_str(
            JSON_BATCH_SPLITTER.join(
                [serialize_json(msg) for msg in msgs]
            ) + JSON_BATCH_SPLITTER,
            compress=self._compress_outbound
        )


class AiohttpMsgPackWebSocketConnection(AiohttpWebSocketConnection):
    async def iterate_msgs(self):
        async for ws_msg in self._ws:
            if ws_msg.type == WSMsgType.BINARY:
                yield msgpack.unpackb(ws_msg.data, use_list=False)

    async def send_msg(self, msg):
        msg_bytes = msgpack.packb(msg)
        await self._ws.send_bytes(
            msg_bytes,
            compress=self._compress_outbound
        )


class AiohttpBatchedMsgPackWebSocketConnection(AiohttpWebSocketConnection):
    async def iterate_msgs(self):
        async for ws_msg in self._ws:
            if not ws_msg.type == WSMsgType.BINARY:
                continue

            for msg in objects_from_msgpack_batch(ws_msg.data):
                yield msg

    async def send_msg(self, msg):
        msg_bytes = msgpack.packb(msg)
        msg_len_bytes = pack_uint32_be(len(msg_bytes))
        await self._ws.send_bytes(
            msg_len_bytes + msg_bytes,
            compress=self._compress_outbound
        )

    async def send_msgs(self, msgs):
        batch_bytes = bytearray()
        for msg in msgs:
            msg_bytes = msgpack.packb(msg)
            msg_len_bytes = pack_uint32_be(len(msg_bytes))
            batch_bytes += msg_len_bytes
            batch_bytes += msg_bytes
        await self._ws.send_bytes(
            batch_bytes,
            compress=self._compress_outbound
        )


ws_protocol_connection_classes = {
    'wamp.2.msgpack': AiohttpMsgPackWebSocketConnection,
    'wamp.2.msgpack.batched': AiohttpBatchedMsgPackWebSocketConnection,
    'wamp.2.json': AiohttpJSONWebSocketConnection,
    'wamp.2.json.batched': AiohttpBatchedJSONWebSocketConnection
}
