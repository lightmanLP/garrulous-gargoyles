from typing import Protocol


class HasSides(Protocol):
    """Proto of object that has sides attributes"""

    top: int
    bottom: int
    left: int
    right: int
