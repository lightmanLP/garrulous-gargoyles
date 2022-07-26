"""Implements utility functions"""

import random

from . import structures as struct


def random_position(x: int | None = None, y: int | None = None) -> tuple[int, int]:
    """
    Get a random position on the game window

    Parameters
    ----------
    x : int, optional
        predefined x-coordinate, randomly generated if None
    y : int, optional
        predefined y-coordinate, randomly generated if None

    Returns
    -------
    tuple[int, int] :
        a random coordinate from the game window
    """
    return (
        random.randrange(struct.WIDTH) if x is None else x,
        random.randrange(struct.HEIGHT) if y is None else y
    )
