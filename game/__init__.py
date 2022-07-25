from .game import Game
from .logging import log

logger = log.getLogger("runner")


def run():
    logger.info("Starting the game")
    Game().mainloop()
    logger.info("Exiting the game")
