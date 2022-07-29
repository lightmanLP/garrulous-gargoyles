import pygame

from .. import structures as struct
from ..event_manager import event_manager
from . import event_handlers  # noqa: F401
from .game import Game

__all__ = ("Game", )


@event_manager.on("draw")
def draw(game: Game):
    """Draw the sprites onto the game window"""
    game.screen.fill(struct.Color.EMERALD)
    game.sprites.draw(game.screen)

    # masks draw
    # for sprite in game.sprites:
    #     if not isinstance(sprite, Object):
    #         continue
    #     olist = tuple(
    #         (sprite.rect.x + x, sprite.rect.y + y)
    #         for x, y in sprite.mask.outline()
    #     )
    #     pygame.draw.polygon(game.screen, struct.Color.BLACK, olist, 0)

    font = pygame.font.SysFont("None", 40)
    text = font.render("Hello World!", True, struct.Color.GREEN.rgba)
    game.screen.blit(text, (300, 300))
