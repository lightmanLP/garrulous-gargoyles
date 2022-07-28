from .serve import Server
from .event import EventHandler


if __name__ == "__main__":
    server = Server("localhost", 8765, EventHandler())
    server.start()
