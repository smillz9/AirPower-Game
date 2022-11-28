import pygame
from pygame.sprite import Sprite


class ShipTwoBullet(Sprite):
    """class for bullets fired from ship"""

    def __init__(self, ap_game):
        super().__init__()
        self.screen = ap_game.screen

        # settings
        self.bullet_speed = 15
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 6

        self.rect = pygame.Rect(0, 0, self.bullet_height, self.bullet_width)
        self.rect.midright = ap_game.ship_two.rect.midright

        self.x = float(self.rect.x)

    def update(self):
        """move bullet on screen"""
        self.x += self.bullet_speed

        self.rect.x = self.x

    def draw_bullet(self):
        """draw bullet on screen"""
        pygame.draw.rect(self.screen, self.bullet_color, self.rect)