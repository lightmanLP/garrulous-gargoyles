from ..event_manager import event_manager
from .. import structures as struct
from ..entities import Object
from .game import Game
from . import event_handlers

import pygame

__all__ = ("Game", )


@event_manager.on("draw")
def draw(game: Game):
    """Draw the sprites onto the game window"""
    # toggle masks
    mask = True
    game.screen.fill(struct.Color.EMERALD)
    game.sprites.draw(game.screen)
    if mask:
        for sprite in game.sprites:
            sprite: Object
            # print(sprite.mask)
            olist = sprite.mask.outline()
            # print(olist)
            pygame.draw.polygon(game.screen, struct.Color.BLACK, olist, 0)
    font = pygame.font.SysFont("None", 40)
    text = font.render("Hello World!", True, struct.Color.GREEN.rgba)
    game.screen.blit(text, (300, 300))
