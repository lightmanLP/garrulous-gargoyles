from typing import Protocol


class HasSides(Protocol):
    top: int
    bottom: int
    left: int
    right: int
