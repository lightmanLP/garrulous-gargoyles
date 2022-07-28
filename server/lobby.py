from typing import Dict
import hashlib
import random
from player import Player


class Lobby:
    """Group a collection of players in a lobby"""

    def __init__(self, name: str):
        salt = random.randbytes(16)
        self.id = hashlib.md5(salt + name.encode()).hexdigest()
        self.name = name
        self.players: dict[str, Player] = {}

    def add_player(self, player: Player):
        """Add a player to the lobby"""
        self.players[player.id] = player

    def remove_player(self, player_id) -> Player:
        """Remove a player from the lobby and return it"""
        return self.players.pop(player_id)


class LobbyManager:
    """Manage lobbies for a whole server"""

    def __init__(self):
        self.lobbies: Dict[str, Lobby] = {}

    def create_lobby(self, name: str) -> Lobby:
        """Create a new lobby"""
        lobby = Lobby(name)
        self.lobbies[lobby.id] = lobby
        return lobby

    def delete_lobby(self, lobby: Lobby) -> None:
        """Delete a lobby"""
        del self.lobbies[lobby.id]

    def add_player_to_lobby(self, player: Player, lobby: Lobby) -> None:
        """Add a player to a lobby"""
        self.lobbies[lobby.id].add_player(player)

    def remove_player_from_lobby(self, player_id: str) -> Player:
        """Remove a player from a lobby and return it"""
        lobby = self.find_player_lobby(player_id)
        player = self.lobbies[lobby.id].remove_player(player_id)
        return player

    def change_player_lobby(self, player_id: str, new_lobby: Lobby) -> None:
        """Change a player's lobby"""
        player = self.remove_player_from_lobby(player_id)
        self.add_player_to_lobby(player, new_lobby)

    def find_player_lobby(self, player_id: str) -> Lobby:
        """Find a player's lobby"""
        for lobby in self.lobbies.values():
            if player_id in lobby.players.keys():
                return lobby
        raise Exception("no existing player in lobbies")
