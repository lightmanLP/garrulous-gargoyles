from os import PathLike

import pygame


class SpriteSheet:
    sheet: pygame.Surface

    def __init__(self, path: PathLike) -> None:
        self.sheet = pygame.image.load(path)

    def image_at(
        self,
        rect: tuple[float, float, float, float] | pygame.Rect
    ) -> pygame.Surface:
        rect = pygame.Rect(rect)
        image = pygame.Surface(rect.size, pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), rect)
        return image
