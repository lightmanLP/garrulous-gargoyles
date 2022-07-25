import pygame


class Entity(pygame.sprite.DirtySprite):
    def __init__(self, file=None, size=(50, 50)):
        super().__init__()
        self.size = size
        if file:
            self.image = pygame.transform.scale(
                pygame.image.load(file), self.size)
            self.rect = self.image.get_rect()

    def spawn(self, pos):
        self.rect.center = pos
        return self

    def move_down(self):
        self.update()

    def move_up(self):
        self.update()

    def move_right(self):
        self.update()

    def move_left(self):
        self.update()
