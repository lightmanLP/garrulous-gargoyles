import websockets
import asyncio


class Server:
    def __init__(self, address, port):
        self.address = address
        self.port = port

    def start(self):
        print("Server listening on port", self.port)
        websockets.serve(self.handle_websocket, self.address, self.port)
        asyncio.run(self.serve())
        print("Server closed")

    async def serve(self):
        server = await websockets.serve(self.handle_websocket, self.address, self.port)
        await server.wait_closed()

    async def handle_websocket(self, websocket, path):
        print("A client connected!")

        async for message in websocket:
            print("Received:", message)
            await websocket.send("Pong: " + message)


server = Server("localhost", 8765)
server.start()
