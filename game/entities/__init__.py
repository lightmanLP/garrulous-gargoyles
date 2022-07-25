import random

import pygame

from ..structures import HEIGHT, WIDTH
from ..utils import random_position
from .entity import Entity
from .spritesheet import SpriteSheet


class Object(Entity):
    def __init__(self, file, size=(50, 50), randomise_size=False):
        super().__init__(file, size)
        self.randomise_size = randomise_size
        self.original_size = size
        self._randomise_size()

    def _randomise_size(self):
        if self.randomise_size:
            self.size = tuple(map(
                lambda axis: (random.randrange(50, 100) * axis) // 100, self.original_size
            ))
        else:
            self.size = self.original_size

    def move_down(self):
        self.rect.y -= 5
        if self.rect.top < 0:
            self._randomise_size()
            self.rect.center = (random_position()[0], HEIGHT)

    def move_up(self):
        self.rect.y += 5
        if self.rect.bottom > HEIGHT:
            self._randomise_size()
            self.rect.center = (random_position()[0], 0)

    def move_right(self):
        self.rect.x -= 5
        if self.rect.left < 0:
            self._randomise_size()
            self.rect.center = (WIDTH, random_position()[0])

    def move_left(self):
        self.rect.x += 5
        if self.rect.right > WIDTH:
            self._randomise_size()
            self.rect.center = (0, random_position()[1])


class Player(Entity):
    def __init__(self, size=(50, 50), init=(0, 0)):
        super().__init__(size=size)
        self.speed = 10
        self.sprite_size = (16, 16)
        self.sheet = SpriteSheet("game/resources/images/sprites/player/moves_b.png")
        self.image = self._get_sprite(*init)
        self.rect = self.image.get_rect()
        self.move_state = 0

    def _get_sprite(self, *position):
        return pygame.transform.scale(
            self.sheet.image_at((
                (position[0] // self.speed) * 16, position[1] * 16,
                *self.sprite_size)), self.size)

    def change_state(self):
        self.move_state = (self.move_state + 1) % (4 * self.speed)

    def move_up(self):
        self.image = self._get_sprite(self.move_state, 1)
        self.change_state()

    def move_down(self):
        self.image = self._get_sprite(self.move_state, 0)
        self.change_state()

    def move_left(self):
        self.image = self._get_sprite(self.move_state, 3)
        self.change_state()

    def move_right(self):
        self.image = self._get_sprite(self.move_state, 2)
        self.change_state()


class Group(pygame.sprite.LayeredUpdates):
    def __init__(self):
        super().__init__()
        print(self.layers())

    def move_up(self):
        for sprite in self.sprites():
            sprite.move_up()

    def move_down(self):
        for sprite in self.sprites():
            sprite.move_down()

    def move_left(self):
        for sprite in self.sprites():
            sprite.move_left()

    def move_right(self):
        for sprite in self.sprites():
            sprite.move_right()
