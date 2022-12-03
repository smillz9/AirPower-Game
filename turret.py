import random

import pygame
from pygame.sprite import Sprite
from turret_bullets import TurretBullet


class Turret(Sprite):

    def __init__(self, position):
        super().__init__()
        self.turret_health = 25

        # the first turret
        self.image = pygame.image.load("turret.png")
        self.rect = self.image.get_rect()
        self.rect.center = position

        # Store decimal value for turret's horizontal and vertical position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def show_damage(self):
        self.image = pygame.image.load("hurt_turret.png")

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y


