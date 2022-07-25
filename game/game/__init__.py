from pygame.constants import *
import pygame

from .. import structures as struct
from ..entities import Group, Object, Player
from ..logging import log
from ..utils import random_position

logger = log.getLogger("game")


class Grass(Object):
    def __init__(self, *args, **kwargs):
        super().__init__("game/resources/images/sprites/grass/grass.png", *args, **kwargs)
        self.level = -20


class Stone(Object):
    def __init__(self, *args, **kwargs):
        super().__init__("game/resources/images/sprites/stone/stone.png", *args, **kwargs)
        self.level = -20


class Tree(Object):
    def __init__(self, *args, **kwargs):
        super().__init__("game/resources/images/sprites/trees/tree.png", *args, **kwargs)
        self.level = 20


# pylint: disable=no-member
class Game:
    running: bool
    screen: pygame.Surface
    clock: pygame.time.Clock
    sprites: Group

    def __init__(self) -> None:
        logger.info("Initiating game")
        pygame.init()

        self.running = False
        self.screen_size = struct.SCREEN_SIZE
        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()
        self.sprites = Group()
        self.generate_background()
        self.sprites.add(Player().spawn(struct.CENTER))

    def generate_background(self):
        # generate 20 grass objects, 20 stones, 10 trees
        grass = [Grass(randomise_size=True).spawn(random_position()) for _ in range(20)]
        stones = [Stone(randomise_size=True).spawn(random_position()) for _ in range(20)]
        trees = [Tree(size=(150, 150)).spawn(random_position()) for _ in range(10)]
        self.sprites.add(*grass, *stones, *trees)

    def keys(self):
        key = pygame.key.get_pressed()
        if key[K_ESCAPE]:
            self.running = False
        elif key[K_DOWN]:
            self.sprites.move_down()
        elif key[K_UP]:
            self.sprites.move_up()
        elif key[K_LEFT]:
            self.sprites.move_left()
        elif key[K_RIGHT]:
            self.sprites.move_right()

    def main(self):
        logger.info("Staring main game loop")
        self.running = True
        key_flag = False
        hold = True
        while self.running:
            for e in pygame.event.get():
                if e.type == QUIT:
                    self.running = False
                if e.type == KEYDOWN:
                    key_flag = True
                    if not hold:
                        self.keys()
                if e.type == KEYUP:
                    key_flag = False
            if key_flag and hold:
                self.keys()

            self.screen.fill(struct.Color.BACKGROUND)

            self.sprites.draw(self.screen)

            font = pygame.font.SysFont("None", 40)
            text = font.render("Hello World!", True, struct.Color.GREEN.rgba)
            self.screen.blit(text, (300, 300))
            pygame.display.update()
            self.clock.tick(60)

        logger.info("Terminating main game loop")
