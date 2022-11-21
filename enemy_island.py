import pygame
from pygame.sprite import Sprite


class EnemyIsland(Sprite):

    def __init__(self, ap_game):
        super().__init__()
        self.screen = ap_game.screen
        self.image = pygame.surface.Surface((320, 512))  # set dimensions for enemy island

        self.rect = self.image.get_rect()

        self.screen_rect = self.screen.get_rect()

        self.dirt = pygame.image.load("dirt.png")
        self.dirt_rect = self.dirt.get_rect()

    def move(self, coordinate):
        self.rect.center = coordinate

    def blitme(self):
        self.draw_enemyisland()
        self.screen.blit(self.image, self.rect)

    def draw_enemyisland(self):

        for y in range(0, 512, 32):
            for x in range(0, 320, 32):
                self.image.blit(self.dirt, (x, y))

