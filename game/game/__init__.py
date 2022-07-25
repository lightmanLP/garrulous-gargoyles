from pygame import constants as pgconst
import pygame

from .. import structures as struct, utils
from ..entities import Group, Object, Player
from ..logging import log

logger = log.getLogger("game")


class Grass(Object):
    def __init__(
        self,
        randomise_size: bool = True,
        level: int = -20,
        **kwargs
    ) -> None:
        super().__init__(
            struct.SPRITES_PATH / "grass" / "grass.png",
            randomise_size=randomise_size,
            **kwargs
        )
        self.level = level


class Stone(Object):
    def __init__(
        self,
        randomise_size: bool = True,
        level: int = -20,
        **kwargs
    ) -> None:
        super().__init__(
            struct.SPRITES_PATH / "stone" / "stone.png",
            randomise_size=randomise_size,
            **kwargs
        )
        self.level = level


class Tree(Object):
    def __init__(
        self,
        size: tuple[int, int] = (150, 150),
        level: int = 20,
        **kwargs
    ) -> None:
        super().__init__(
            struct.SPRITES_PATH / "trees" / "tree.png",
            size=size,
            **kwargs
        )
        self.level = level


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
        self.screen = pygame.display.set_mode(struct.SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.sprites = Group()

        self.generate_background()
        self.sprites.add(Player().spawn(struct.CENTER))

    def generate_background(self):
        self.sprites.add(
            *(Grass().random_spawn() for _ in range(20)),
            *(Stone().random_spawn() for _ in range(20)),
            *(Tree().random_spawn() for _ in range(10)),
        )

    def keys(self):
        key = pygame.key.get_pressed()
        if key[pgconst.K_ESCAPE]:
            self.running = False
        elif key[pgconst.K_DOWN]:
            self.sprites.move(struct.Direction.DOWN)
        elif key[pgconst.K_UP]:
            self.sprites.move(struct.Direction.UP)
        elif key[pgconst.K_LEFT]:
            self.sprites.move(struct.Direction.LEFT)
        elif key[pgconst.K_RIGHT]:
            self.sprites.move(struct.Direction.RIGHT)

    def main(self):
        logger.info("Staring main game loop")
        self.running = True
        key_flag = False
        hold = True
        while self.running:
            for e in pygame.event.get():
                if e.type == pgconst.QUIT:
                    self.running = False
                if e.type == pgconst.KEYDOWN:
                    key_flag = True
                    if not hold:
                        self.keys()
                if e.type == pgconst.KEYUP:
                    key_flag = False
            if key_flag and hold:
                self.keys()

            self.screen.fill(struct.Color.EMERALD)

            self.sprites.draw(self.screen)

            font = pygame.font.SysFont("None", 40)
            text = font.render("Hello World!", True, struct.Color.GREEN.rgba)
            self.screen.blit(text, (300, 300))
            pygame.display.update()
            self.clock.tick(60)

        logger.info("Terminating main game loop")
