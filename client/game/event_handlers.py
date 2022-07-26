from typing import TYPE_CHECKING

import pygame

from .. import structures as struct
from ..event_manager import event_manager

if TYPE_CHECKING:
    from . import Game


MOVEMENT_BINDS: dict[int, struct.Direction] = {
    pygame.K_UP: struct.Direction.UP,
    pygame.K_LEFT: struct.Direction.LEFT,
    pygame.K_DOWN: struct.Direction.DOWN,
    pygame.K_RIGHT: struct.Direction.RIGHT,
    pygame.K_w: struct.Direction.UP,
    pygame.K_a: struct.Direction.LEFT,
    pygame.K_s: struct.Direction.DOWN,
    pygame.K_d: struct.Direction.RIGHT,
}


@event_manager.on(pygame.QUIT)
def quit(game: "Game", e: "pygame.event.Event | None" = None):
    """Quits the game on pygame.QUIT"""
    game.quit()


@event_manager.on(pygame.KEYDOWN)
def per_press_binds(game: "Game", e: pygame.event.Event):
    """Binds that are activated at the moment of pressing"""
    key: int = e.key
    match key:
        case pygame.K_ESCAPE:
            game.quit()


@event_manager.on("tick")
def passive_binds(game: "Game"):
    """Binds that remain active all the time you hold button"""
    pressed = pygame.key.get_pressed()
    for key, direction in MOVEMENT_BINDS.items():
        if not pressed[key]:
            continue
        game.sprites.move(direction)
        break
