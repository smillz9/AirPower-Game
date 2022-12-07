import pygame
from pygame.sprite import Sprite


class HomeHangar(Sprite):

    def __init__(self, ap_game):
        super().__init__()
        self.screen = ap_game.screen
        self.screen_rect = ap_game.screen.get_rect()
        self.health = 45
        self.healthy_image = pygame.image.load("home_hangar_bay.png")
        self.hurt_image = pygame.image.load("hurt_home_hangar.png")
        self.image = self.healthy_image

        self.rect = self.image.get_rect()
        self.rect.center = (256,320)

        # store value for hangars static position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def show_damage(self):
        self.image = self.hurt_image
