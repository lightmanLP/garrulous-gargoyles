import hashlib
import random

from lobby import Lobby


class Player:
    def __init__(self, name: str, lobby: Lobby):
        self.name: str = name
        salt = random.randbytes(16)
        self.id = hashlib.md5(salt + name.encode()).hexdigest()
        self.lobby: Lobby = lobby

    def change_lobby(self, lobby: Lobby):
        self.lobby.remove_player(self.id)
        lobby.add_player(self)
        self.lobby = lobby
