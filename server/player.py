import numpy as np
from typing import TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from .lobby import Lobby


class Player:
    """Store data about players"""

    name: str
    id: bytes
    _lobby: "Lobby | None" = None
    location: np.ndarray = np.zeros((2,), dtype=np.float64)

    def __init__(self, name: str) -> None:
        self.name = name
        self.id = uuid.uuid1().bytes

    @property
    def lobby(self) -> "Lobby | None":
        return self._lobby

    @lobby.setter
    def lobby(self, lobby: "Lobby | None"):
        self._lobby = lobby

    def leave(self):
        self.lobby.remove_player(self.id)
