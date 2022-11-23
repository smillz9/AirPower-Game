import pygame
from pygame.sprite import Sprite


class HomeIsland(Sprite):

    def __init__(self, ap_game):
        super().__init__()
        self.screen = ap_game.screen
        self.screen_rect = ap_game.screen.get_rect()
        self.grass = pygame.image.load("grass.png")
        self.image = pygame.surface.Surface((320, 512))  # set dimensions for home island
        self.rect = self.image.get_rect()

    def move(self, coordinate):
        self.rect.center = coordinate

    def blitme(self):
        self.draw_homeisland()
        self.screen.blit(self.image, self.rect)

    def draw_homeisland(self):
        for y in range(0, 512, 32):
            for x in range(0, 320, 32):
                self.image.blit(self.grass, (x, y))



