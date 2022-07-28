import websockets
import asyncio
import json


def parse_data(data):
    return json.loads(data)


def serialize_data(data):
    return json.dumps(data)


async def print_hello(*args, **kwargs):
    print("Hello World!")


async def print_bye(*args, **kwargs):
    print("Goodbye World!")


class Server:
    def __init__(self, address, port, event_handler):
        self.address = address
        self.port = port
        self.event_handler = event_handler
        self.setup_events()

    def setup_events(self):
        eh = self.event_handler
        eh.register("enter", print_hello)
        eh.register("leave", print_bye)

    def start(self):
        try:
            asyncio.run(self.serve())
        except KeyboardInterrupt:
            print("Server stopped.")
            return

    async def serve(self):
        print(f"[LOG] Server listening on {self.address}:{self.port}")

        async with websockets.serve(self.handle_websocket, self.address, self.port):
            await asyncio.Future()

        print("[LOG] Server closed")

    async def handle_websocket(self, websocket, path):
        while True:
            try:
                data = await websocket.recv()  # Should received a dictionary like string
            except websockets.ConnectionClosedOK:
                await self.event_handler.handle_event("leave", websocket)
                break

            data = parse_data(data)  # now a dictionary
            print(f"[LOG] Received: {data}")
            await self.event_handler.handle_event(data["type"], data, websocket)
