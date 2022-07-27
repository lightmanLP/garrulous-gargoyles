from os import PathLike

import pygame


class SpriteSheet:
    """Class for sprite-sheets"""

    sheet: pygame.Surface

    def __init__(self, path: PathLike) -> None:
        self.sheet = pygame.image.load(path)

    def image_at(self, rect: tuple[int, int, int, int] | pygame.Rect) -> pygame.Surface:
        """Get sprite image at the specified frame (a rectangle)"""
        rect = pygame.Rect(rect)
        image = pygame.Surface(rect.size, pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), rect)
        return image
