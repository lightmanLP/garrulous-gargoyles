import hashlib
import random


class Lobby:
    def __init__(self, lobby_id, lobby_name):
        self.lobby_id = lobby_id
        self.lobby_name = lobby_name
        self.players: dict[str, Player] = {}

    def add_player(self, player):
        self.players[player.id] = player

    def remove_player(self, player_id):
        del self.players[player_id]


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
