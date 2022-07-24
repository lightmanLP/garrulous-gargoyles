import pygame

from .. import structures as struct


class Game:
    running: bool
    screen: pygame.Surface
    clock: pygame.time.Clock

    def __init__(self) -> None:
        print("Initiating game")
        pygame.init()

        self.running = False
        self.screen = pygame.display.set_mode(struct.SCREEN_SIZE)
        self.clock = pygame.time.Clock()

    def main(self):
        print("Staring main game loop")
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.screen.fill(struct.Color.WHITE)

            font = pygame.font.SysFont("None", 40)
            text = font.render("Hello World!", True, struct.Color.GREEN)
            self.screen.blit(text, (300, 300))
            pygame.display.update()
            self.clock.tick(60)

        print("Terminating main game loop")
