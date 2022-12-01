import pygame
from pygame.sprite import Sprite


class TurretBullet(Sprite):
    """class for bullets fired from 1st turret"""

    def __init__(self, position, vector):
        super().__init__()

        # settings
        self.bullet_speed = 15
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 6

        self.x_speed = 15*vector[0]
        self.y_speed = 15*vector[1]

        self.image = pygame.surface.Surface((self.bullet_height, self.bullet_width))
        self.image.fill(self.bullet_color)
        self.rect = self.image.get_rect()
        self.rect.center = position

    def update(self):
        """move bullet on screen"""
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

    def draw(self, screen):
        """draw bullet on screen"""
        pygame.draw.rect(screen, self.bullet_color, self.rect)
