import websockets
import asyncio

PORT = 8765

print("Server listening on port", PORT)


async def echo(websocket, path):
    """It echos."""
    print("A client connected!")

    async for message in websocket:
        print("Received:", message)
        await websocket.send("Pong: " + message)


async def serve():
    """It serves."""
    server = await websockets.serve(echo, 'localhost', 8765)
    await server.wait_closed()


websockets.serve(echo, "localhost", PORT)
asyncio.run(serve())
print("Server closed")
