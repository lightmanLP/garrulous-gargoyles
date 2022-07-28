import asyncio

from . import event_handlers
from .serve import Server


def run():
    loop = asyncio.get_event_loop_policy().get_event_loop()
    loop.create_task(Server().serve("localhost", 8765))
    loop.run_forever()
