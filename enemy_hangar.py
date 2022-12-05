import pygame
from pygame.sprite import Sprite


class EnemyHangar(Sprite):

    def __init__(self, ap_game):
        super().__init__()
        self.screen = ap_game.screen
        self.screen_rect = ap_game.screen.get_rect()
        self.health = 250
        self.healthy_image = pygame.image.load("enemy_hangar.png")
        self.hurt_image = pygame.image.load("hurt_enemyhangar.png")
        self.image = self.healthy_image

        self.rect = self.image.get_rect()
        self.rect.center = (1000,320)

        # store value for hangars static position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def show_damage(self):
        self.image = self.hurt_image
