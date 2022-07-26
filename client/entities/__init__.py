from typing import TYPE_CHECKING, Any
from abc import ABC
from os import PathLike
import random

import pygame

from .. import structures as struct
from .. import utils
from .entity import Entity
from .spritesheet import SpriteSheet

if TYPE_CHECKING:
    from typing_extensions import Self


class Movable(ABC):
    """Abstract base class for movable entities"""

    def move(self, direction: struct.Direction) -> Any:
        """Move the entity in the given direction"""


class Object(Entity, Movable):
    """Objects on the game window other than the player and UI components"""

    randomise_size: bool
    original_size: tuple[int, int]

    def __init__(
        self,
        path: PathLike,
        size: tuple[int, int] = (50, 50),
        randomise_size: bool = False,
    ) -> None:
        super().__init__(path, size)
        self.randomise_size = randomise_size
        self.original_size = size
        self._randomise_size()

    def _randomise_size(self):
        """Randomises the object size"""
        if self.randomise_size:
            self.size = tuple(
                (random.randrange(50, 100) * axis) // 100 for axis in self.original_size
            )
        else:
            self.size = self.original_size

    def move(self, direction: struct.Direction) -> "Self":
        """Move the object in the given direction"""
        shift = direction.sign * struct.OBJECT_STEP
        match direction:
            case struct.Direction.UP | struct.Direction.DOWN:
                self.rect.y += shift
            case struct.Direction.LEFT | struct.Direction.RIGHT:
                self.rect.x += shift

        if not direction.opposite.is_in_rect(struct.SCREEN_RECT, self.rect):
            self._randomise_size()
            fixed_coord = struct.SCREEN_RECT[direction]
            if direction.pos_i == 0:
                self.rect.center = utils.random_position(x=fixed_coord)
            else:
                self.rect.center = utils.random_position(y=fixed_coord)
        return self

    def random_spawn(self) -> "Self":
        """Spawn the object at a random position"""
        return self.spawn(utils.random_position())


class Player(Entity, Movable):
    """Player object"""

    speed: int
    sprite_size: tuple[int, int]
    sheet: SpriteSheet
    move_state: int

    def __init__(
        self,
        size: tuple[int, int] = (50, 50),
        init: tuple[int, int] = (0, 0)
    ) -> None:
        super().__init__(size=size)

        self.speed = 10
        self.sprite_size = (16, 16)
        self.sheet = SpriteSheet(struct.SPRITES_PATH / "player" / "moves_b.png")
        self.move_state = 0

        self.image = self._get_sprite(init)
        self.rect = self.image.get_rect()

    def _get_sprite(self, position: tuple[int, int]) -> pygame.Surface:
        return pygame.transform.scale(
            self.sheet.image_at(
                (
                    (position[0] // self.speed) * 16,
                    position[1] * 16,
                    *self.sprite_size
                )
            ),
            self.size,
        )

    def move(self, direction: struct.Direction) -> "Self":
        """Move the player in the given direction"""
        self.image = self._get_sprite((self.move_state, direction.value))
        self.move_state = (self.move_state + 1) % (4 * self.speed)
        return self


class Group(pygame.sprite.LayeredUpdates, Movable):
    """Group of sprites, can be layered"""

    def move(self, direction: struct.Direction) -> "Self":
        """Move the members of this group in the given direction"""
        for sprite in self.sprites():
            if isinstance(sprite, Movable):
                sprite.move(direction)
        return self
