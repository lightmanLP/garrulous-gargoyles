import pygame
import logging

from ..config import Color, screen


class Game:
    def __init__(self):
        logging.info("Initiating game")
        pygame.game = self
        self.running = False
        self.screen = screen
        self.clock = pygame.time.Clock()

    def main(self):
        logging.info("Staring main game loop")
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.screen.fill(Color.white)

            font = pygame.font.SysFont("None", 40)
            text = font.render("Hello World!", True, Color.green)
            self.screen.blit(text, (300, 300))
            pygame.display.update()
            self.clock.tick(60)

        logging.info("Terminating main game loop")
