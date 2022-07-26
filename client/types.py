from typing import Protocol


class HasSides(Protocol):
    """TODO:"""

    top: int
    bottom: int
    left: int
    right: int
