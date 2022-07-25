import random

from . import structures as struct


def random_position(x: int | None = None, y: int | None = None) -> tuple[int, int]:
    return (
        random.randrange(struct.WIDTH) if x is None else x,
        random.randrange(struct.HEIGHT) if y is None else y
    )
