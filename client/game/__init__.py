from typing import NoReturn

import pygame

from .. import structures as struct
from ..entities import Group, Player
from ..event_manager import event_manager
from ..logging import log
from . import event_handlers  # noqa: F401
from .objects import Grass, Stone, Tree

logger = log.getLogger("game")


class Game:
    """The game class, all core logic is defined here or called from here"""

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

        self._generate_background()
        self.sprites.add(Player().spawn(struct.CENTER))

    def _generate_background(self):
        """Generates the background"""
        self.sprites.add(
            *(Grass().random_spawn() for _ in range(20)),
            *(Stone().random_spawn() for _ in range(20)),
            *(Tree().random_spawn() for _ in range(10)),
        )
        logger.info("Background generated")

    def mainloop(self) -> NoReturn:
        """The game main loop"""
        logger.info("Staring main game loop")
        self.running = True

        while self.running:
            for e in pygame.event.get():
                event_manager.emit(e.type, self, e)
            event_manager.emit("tick", self)
            event_manager.emit("draw", self)
            pygame.display.update()
            self.clock.tick(60)

        logger.info("Terminating main game loop")

    def quit(self):
        """Quit the game"""
        self.running = False


@event_manager.on("draw")
def draw(game: Game):
    """Draw the sprites onto the game window"""
    game.screen.fill(struct.Color.EMERALD)
    game.sprites.draw(game.screen)

    font = pygame.font.SysFont("None", 40)
    text = font.render("Hello World!", True, struct.Color.GREEN.rgba)
    game.screen.blit(text, (300, 300))
