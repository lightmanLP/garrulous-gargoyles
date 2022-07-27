import websockets
import asyncio


class Client:
    def __init__(self, address, port):
        self.address = address
        self.port = port

    def start(self):
        asyncio.run(self.listen())

    async def listen(self):
        url = f"ws://{self.address}:{self.port}"

        async with websockets.connect(url) as ws:
            await ws.send({"type": "enter"})
            while True:
                msg = await ws.recv()
                print(msg)


client = Client("localhost", 8765)
client.start()
