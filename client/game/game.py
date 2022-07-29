from typing import TYPE_CHECKING, ClassVar, NoReturn

import pygame

from .. import structures as struct
from ..entities import Blocking, Collidable, Entity, Group, Player
from ..event_manager import event_manager
from ..logging import log
from .entities import Grass, Stone, Tree

if TYPE_CHECKING:
    from typing_extensions import Self

logger = log.getLogger("game")


class ScreenGroup(Group):
    """Group of sprites on the screen"""

    def move(self, direction: struct.Direction, exclude=None) -> "Self":
        """Move the member sprites"""
        game = Game.get()

        prediction = Entity()
        p_rect = game.player.rect.copy()
        p_rect.x, p_rect.y = direction.opposite.move(
            p_rect.x, p_rect.y,
            struct.COLLISION_DISTANCE
        )
        prediction.rect = p_rect
        prediction.mask = game.player.mask.copy()
        exclude = [] if exclude is None else exclude

        for sprite in self.sprites():
            if (
                sprite is game.player
                or not isinstance(sprite, Collidable)
                or not pygame.sprite.collide_mask(sprite, prediction)
            ):
                continue
            if not all(event_manager.emit("collide", game, sprite)):
                return self
            if isinstance(sprite, Blocking):
                exclude.append(sprite)

        return super().move(direction, exclude=exclude)


class Game:
    """The game class, all core logic is defined here or called from here"""

    _instance: ClassVar["type[Self] | None"] = None

    running: bool
    screen: pygame.Surface
    clock: pygame.time.Clock
    sprites: ScreenGroup

    def __new__(cls: type["Self"], *args, **kwargs) -> "Self":
        """TODO: fixme"""
        assert cls._instance is None
        cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        logger.info("Initiating game")
        pygame.init()

        self.running = False
        self.screen = pygame.display.set_mode(struct.SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.sprites = ScreenGroup()

        self._generate_background()
        self.player = Player().spawn(struct.CENTER)
        self.sprites.add(self.player)

    @classmethod
    def get(cls) -> "Self":
        """Get the game instance"""
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


@event_manager.on("draw")
def draw(game: Game):
    """Draw the sprites onto the game window"""
    game.screen.fill(struct.Color.EMERALD)
    game.sprites.draw(game.screen)

    # masks draw
    # for sprite in game.sprites:
    #     if not isinstance(sprite, (Object, Player)):
    #         continue
    #     olist = tuple(
    #         (sprite.rect.x + x, sprite.rect.y + y)
    #         for x, y in sprite.mask.outline()
    #     )
    #     pygame.draw.polygon(game.screen, struct.Color.BLACK, olist, 0)

    font = pygame.font.SysFont("None", 40)
    text = font.render("Hello World!", True, struct.Color.GREEN.rgba)
    game.screen.blit(text, (300, 300))
