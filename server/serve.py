import websockets
import asyncio
import json


def print_hello():
    print("Hello World!")


def print_bye():
    print("Goodbye World!")


class Server:
    def __init__(self, address, port, event_handler):
        self.address = address
        self.port = port
        self.event_handler = event_handler

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
        print(f"Server listening on {self.address}:{self.port}")

        async with websockets.serve(self.handle_websocket, self.address, self.port):
            await asyncio.Future()

        print("Server closed")

    async def handle_websocket(self, websocket, path):
        while True:
            try:
                message = await websocket.recv()  # Should received a dictionary like string
            except websockets.ConnectionClosedOK:
                self.event_handler.handle_event("leave", websocket)
                break

            print("websocket received:", websocket)
            print("message:", message)

            await websocket.send("Pong: " + message)
            self.event_handler.handle_event(message)
