from .game import Game
from .logging import log

logger = log.getLogger("runner")


def run():
    logger.info("Starting the game")
    game = Game()
    game.main()
    logger.info("Exiting the game")
