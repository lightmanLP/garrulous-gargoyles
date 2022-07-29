"""Defines commonly used structures throughout the code"""

from typing import Literal
from enum import IntEnum
from pathlib import Path

from .types import HasSides

WIDTH, HEIGHT = SCREEN_SIZE = (1080, 720)
CENTER = WIDTH // 2, HEIGHT // 2
SCREEN_RECT = (0, 0, *SCREEN_SIZE)

OBJECT_STEP = 5
COLLISION_DISTANCE = OBJECT_STEP + 2

ROOT_PATH = Path.cwd()
RESOURCES_PATH = ROOT_PATH / "resources"
IMAGES_PATH = RESOURCES_PATH / "images"
SPRITES_PATH = IMAGES_PATH / "sprites"


class Color(IntEnum):
    """Commonly used colours"""

    RED = 0xFF0000
    GREEN = 0x00FF00
    BLUE = 0x0000FF
    WHITE = 0xFFFFFF
    BLACK = 0x000000
    EMERALD = 0x4CAF4F

    @property
    def rgba(self) -> int:
        """Returns rgba compatible integer for pygame.Color"""
        return (self.value << 8) + 0xFF


class Direction(IntEnum):
    """The 4 directions"""

    LEFT = 0
    UP = 1
    RIGHT = 2
    DOWN = 3

    @property
    def sign(self) -> int:
        """+/-"""
        return DIRECTIONS_SIGN[self]

    @property
    def side(self) -> str:
        """Get side name"""
        return SIDE_NAMES[self]

    @property
    def opposite(self) -> "Direction":
        """Get the side opposite to current side"""
        return opposite_directions[self]

    @property
    def is_pos_definer(self) -> bool:
        """LEFT | UP"""
        return self.value < 2

    @property
    def pos_i(self) -> Literal[0, 1]:
        """Position index for (x, y) sequences"""
        return self.value & 1

    @property
    def is_vertical(self) -> bool:
        return bool(self.pos_i)

    @property
    def is_horizontal(self) -> bool:
        return not self.is_vertical

    def is_in_rect(self, rect: tuple[int, int, int, int], contains: HasSides) -> bool:
        """Checks if object in some rect after move in this direction"""
        side = getattr(contains, self.opposite.side)
        if self.opposite.is_pos_definer:
            return side <= rect[self.value]
        return side >= rect[self.value]

    def move(self, x: int, y: int, step: int = OBJECT_STEP) -> tuple[int, int]:
        shift = self.sign * step
        if self.is_horizontal:
            x += shift
        else:
            y += shift
        return (x, y)


DIRECTIONS_SIGN: dict[Direction, int] = {
    Direction.UP: 1,
    Direction.DOWN: -1,
    Direction.LEFT: 1,
    Direction.RIGHT: -1
}
SIDE_NAMES: dict[Direction, str] = {
    Direction.UP: "top",
    Direction.DOWN: "bottom",
    Direction.LEFT: "left",
    Direction.RIGHT: "right"
}
opposite_directions: dict[Direction, Direction] = {
    Direction.UP: Direction.DOWN,
    Direction.LEFT: Direction.RIGHT
}
opposite_directions.update({v: k for k, v in opposite_directions.items()})
