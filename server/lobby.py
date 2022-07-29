import uuid

from .player import Player


class Lobby:
    """Group a collection of players in a lobby"""

    id: bytes
    players: dict[bytes, Player]

    def __init__(self) -> None:
        self.id = uuid.uuid1().bytes
        self.players = dict()

    def add_player(self, player: Player):
        """Add a player to the lobby"""
        self.players[player.id] = player
        player.lobby = self

    def remove_player(self, player_id: bytes) -> Player:
        """Remove a player from the lobby and return it"""
        player = self.players.pop(player_id)
        player.lobby = None
        return player

    def __del__(self):
        for player in self.players.values():
            player.lobby = None


class LobbyManager:
    """Manage lobbies for a whole server"""

    lobbies: dict[bytes, Lobby]

    def __init__(self) -> None:
        self.lobbies = dict()

    def create_lobby(self) -> Lobby:
        """Create a new lobby"""
        lobby = Lobby()
        self.lobbies[lobby.id] = lobby
        return lobby

    def delete_lobby(self, lobby: Lobby):
        """Delete a lobby"""
        del self.lobbies[lobby.id]

    def add_player_to_lobby(self, player: Player, lobby_id: bytes):
        """Add a player to a lobby"""
        self.lobbies[lobby_id].add_player(player)

    # def find_player_lobby(self, player_id: str) -> Lobby:
    #     """Find a player's lobby"""
    #     for lobby in self.lobbies.values():
    #         if player_id in lobby.players.keys():
    #             return lobby
    #     raise Exception("no existing player in lobbies")
