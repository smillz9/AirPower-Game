import pygame
from pygame.sprite import Sprite


class HomeIsland(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.image = pygame.surface.Surface((100,320))
        self.image.blit(pygame.image.load("pirate_corner_land.png"),
                        (0,0))
        self.image.blit(pygame.image.load("water.png"),
                        (0,0))

        self.rect = self.image.get_rect()

    def move(self, coordinate):
        self.rect.center = coordinate

    def blitme(self):
        self.screen.blit(self.image, self.rect)

