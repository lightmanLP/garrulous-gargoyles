from typing import TYPE_CHECKING, Any, ClassVar, Container
from abc import ABC
from os import PathLike
import random

import pygame

from .. import structures as struct
from .. import utils
from .entity import Attackable, Blocking, Collectible, Collidable, Entity
from .spritesheet import SpriteSheet

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = (
    "Attackable",
    "Blocking",
    "Collectible",
    "Collidable",
    "Entity",
    "SpriteSheet",
    "Movable",
    "Object",
    "Player",
    "Group",
)


class Movable(ABC):
    """Abstract base class for movable entities"""

    def move(self, direction: struct.Direction) -> Any:
        """Move the entity in the given direction"""


class Object(Entity, Movable):
    """Objects on the game window other than the player and UI components"""

    PATH: ClassVar[PathLike | None] = None
    randomise_size: bool
    original_size: tuple[int, int]

    def __init__(
        self,
        size: tuple[int, int] = (50, 50),
        randomise_size: bool = False,
        layer: int | None = None,
    ) -> None:
        super().__init__(self.__class__.PATH, size)
        if layer is not None:
            self._layer = layer
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
        self._generate_mask()
        # generate a future object
        self.rect.x, self.rect.y = direction.move(self.rect.x, self.rect.y)
        if not direction.opposite.is_in_rect(struct.SCREEN_RECT, self.rect):
            self._randomise_size()
            fixed_coord = (
                struct.SCREEN_RECT[direction]
                - direction.sign * self.size[direction.pos_i] // 2
            )
            if direction.is_horizontal:
                self.rect.center = utils.random_position(x=fixed_coord)
            else:
                self.rect.center = utils.random_position(y=fixed_coord)
        return self

    def random_spawn(self) -> "Self":
        """Spawn the object at a random position"""
        return self.spawn(utils.random_position())


class Player(Movable, Attackable, Entity):
    """Player object"""

    speed: int
    sprite_size: tuple[int, int]
    sheet: SpriteSheet
    move_state: int
    health: int
    inventory: dict

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
        self._generate_mask()

        self.inventory = {}

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
        self._generate_mask()
        self.move_state = (self.move_state + 1) % (4 * self.speed)
        return self


class Group(pygame.sprite.LayeredUpdates, Movable):
    """Group of sprites, can be layered"""

    def move(
        self,
        direction: struct.Direction,
        exclude: Container[pygame.sprite.Sprite] = ()
    ) -> "Self":
        """Move the members of this group in the given direction"""
        for sprite in self.sprites():
            if (
                not isinstance(sprite, Movable)
                or sprite in exclude
            ):
                continue
            sprite.move(direction)
        return self
