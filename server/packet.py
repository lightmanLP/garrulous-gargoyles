import numpy as np
from .player import Player
from .action import Action


# to be sent with send_binary()


def pack(thing) -> list[int]:
    if isinstance(thing, Player):
        data = b"P" + thing.id + thing.location.tobytes()
    elif isinstance(thing, Action):
        data = b"A" + thing.player.id + thing.target.id  # + thing.type
    else:
        raise TypeError("packet: unknown type")

    return list(data)


def unpack(data: list[int]) -> object:
    if data[0] == ord("P"):
        return bytes(data[1:17]), np.frombuffer(bytes(data[17:]), dtype=np.float64)
    elif data[0] == ord("A"):
        return bytes(data[1:17]), bytes(data[17:33]), data[33:]
