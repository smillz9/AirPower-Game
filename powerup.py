import pygame
from pygame.sprite import Sprite


class Powerup(Sprite):

    def __init__(self, position):
        super().__init__()

        # the first turret
        self.image = pygame.image.load("powerup.png")
        self.rect = self.image.get_rect()
        self.rect.center = position

        # Store decimal value for turret's horizontal and vertical position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y

