from typing import TYPE_CHECKING
from os import PathLike

import pygame

if TYPE_CHECKING:
    from typing_extensions import Self


class Entity(pygame.sprite.DirtySprite):
    """An Entity in the game"""

    image: pygame.Surface
    rect: pygame.Rect

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

    def spawn(self, pos: tuple[int, int]) -> "Self":
        """Spawns the entity at the given coordinates"""
        self.rect.center = pos
        return self
