from player import Player


class Lobby:
    def __init__(self, lobby_id, lobby_name):
        self.lobby_id = lobby_id
        self.lobby_name = lobby_name
        self.players: dict[str, Player] = {}

    def add_player(self, player):
        self.players[player.id] = player

    def remove_player(self, player_id):
        del self.players[player_id]
