from typing import TYPE_CHECKING, NoReturn, ClassVar

import pygame

from .. import structures as struct
from ..entities import Group, Player
from ..event_manager import event_manager
from ..logging import log
from .objects import Grass, Stone, Tree

if TYPE_CHECKING:
    from typing_extensions import Self

logger = log.getLogger("game")


class Game:
    """The game class, all core logic is defined here or called from here"""

    _instance: ClassVar["type[Self] | None"] = None

    running: bool
    screen: pygame.Surface
    clock: pygame.time.Clock
    sprites: Group

    def __new__(cls, *args, **kwargs) -> "Self":
        assert cls._instance is None
        cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        logger.info("Initiating game")
        pygame.init()

        self.running = False
        self.screen = pygame.display.set_mode(struct.SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.sprites = Group()

        self._generate_background()
        self.player = Player().spawn(struct.CENTER)
        self.sprites.add(self.player)

    @classmethod
    def get(cls) -> "Self":
        if cls._instance is None:
            return cls()
        return cls._instance

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
