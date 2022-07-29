from typing import TYPE_CHECKING
from abc import ABC
from os import PathLike

import pygame

if TYPE_CHECKING:
    from typing_extensions import Self

    from . import Player


class Entity(pygame.sprite.DirtySprite):
    """An Entity in the game"""

    image: pygame.Surface
    rect: pygame.Rect
    mask: pygame.mask.Mask

    def __init__(
        self,
        path: PathLike | None = None,
        size: tuple[int, int] = (50, 50)
    ) -> None:
        super().__init__()
        self.size = size
        if path is not None:
            self.image = pygame.transform.scale(
                pygame.image.load(path),
                self.size
            )
            self.rect = self.image.get_rect()
            self._generate_mask()

    def spawn(self, pos: tuple[int, int]) -> "Self":
        """Spawns the entity at the given coordinates"""
        self.rect.center = pos
        return self

    def _generate_mask(self):
        self.mask = pygame.mask.from_surface(self.image)


class Collidable(Entity, ABC):
    """Abstracts entities that can collide"""


class Blocking(Collidable, ABC):
    """Abstracts blocking entities"""


class Collectible(Collidable, ABC):
    """Abstracts entities that can be collected"""

    item = None

    def __new__(cls: type["Self"], *args, **kwargs) -> "Self":
        """Validation allocator"""
        assert cls.item is not None
        return super().__new__(cls, *args, **kwargs)

    def collect(self, player: "Player"):  # -> item
        """Collect FROM this entity"""
        player.inventory[self.item] = player.inventory.get(self.item, 0) + 1


class Attackable(Collidable, ABC):
    """Abstracts entities that can be attacked"""

    health = 100  # default

    def attack(self, damage: int) -> int:
        """Attack DEALT ON THIS entity"""
        self.health -= damage
        return self.health
