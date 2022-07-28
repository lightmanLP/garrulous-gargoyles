from typing import NoReturn
import asyncio
import json

from websockets.exceptions import ConnectionClosedOK
from websockets.server import WebSocketServerProtocol
from websockets.server import serve as ws_serve

from .event_manager import event_manager
from .logging import log

logger = log.getLogger("server")


def parse_data(data):
    return json.loads(data)


def serialize_data(data):
    return json.dumps(data)


class Server:
    connections: list[WebSocketServerProtocol]

    def __init__(self) -> None:
        # TODO: make connections a hashmap and use player_id as key
        self.connections = list()

    async def serve(self, address: str, port: int) -> NoReturn:
        async with ws_serve(self.ws_callback, address, port):
            await asyncio.Future()

    async def ws_callback(self, ws: WebSocketServerProtocol):
        self.connections.append(ws)
        try:
            while True:
                try:
                    data = await ws.recv()  # Should received a dictionary like string
                except ConnectionClosedOK:
                    await event_manager.emit("leave", ws)
                    break

                data = parse_data(data)  # now a dictionary
                logger.debug(f"received: {data}")
                event_manager.dispatch(data["type"], ws, data)
        finally:
            self.connections.remove(ws)
