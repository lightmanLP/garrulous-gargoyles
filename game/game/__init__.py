import pygame

import config
from config import Color


class Game:
    def __init__(self):
        print("Initiating game")
        pygame.game = self
        self.running = False
        self.screen = config.screen
        self.clock = pygame.time.Clock()

    def main(self):
        print("Staring main game loop")
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

        print("Terminating main game loop")
