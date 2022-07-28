from . import server
from . import events

Server = server.Server
EventHandler = events.EventHandler

if __name__ == "__main__":
    server = Server("localhost", 8765, EventHandler())
    server.start()
