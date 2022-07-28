from typing import Dict
from player import Player


class Lobby:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
        self.players: dict[str, Player] = {}

    def add_player(self, player: Player):
        self.players[player.id] = player

    def remove_player(self, player_id) -> Player:
        return self.players.pop(player_id)


class LobbyManager:
    def __init__(self):
        self.lobbies: Dict[str, Lobby] = {}

    def create_lobby(self, id: str, name: str) -> Lobby:
        lobby = Lobby(id, name)
        self.lobbies[id] = lobby
        return lobby

    def delete_lobby(self, lobby: Lobby) -> None:
        del self.lobbies[lobby.id]

    def add_player_to_lobby(self, player: Player, lobby: Lobby) -> None:
        self.lobbies[lobby.id].add_player(player)

    def remove_player_from_lobby(self, player_id: str) -> Player:
        lobby = self.find_player_lobby(player_id)
        player = self.lobbies[lobby.id].remove_player(player_id)
        return player

    def change_player_lobby(self, player_id: str, new_lobby: Lobby) -> None:
        player = self.remove_player_from_lobby(player_id)
        self.add_player_to_lobby(player, new_lobby)

    def find_player_lobby(self, player_id: str) -> Lobby:
        for lobby in self.lobbies.values():
            if player_id in lobby.players.keys():
                return lobby
        raise Exception("no existing player in lobbies")
