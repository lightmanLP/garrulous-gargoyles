import pygame


class SpriteSheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file)

    def image_at(self, rectangle):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), rect)
        return image
