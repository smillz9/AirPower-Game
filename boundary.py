import pygame
from pygame.sprite import Sprite


class Boundary(Sprite):
    """class for bullets fired from ship"""

    def __init__(self, ap_game):
        super().__init__()
        self.screen = ap_game.screen

        # settings
        self.boundary_width = 2
        self.boundary_height = 15
        self.bounary_color = (0, 0, 0)
        self.boundary_color_two = (255, 255, 255)

        self.rect = pygame.Rect(0, 0, self.boundary_width, self.boundary_height)

    def draw_boundary(self):
        """draw bullet on screen"""
        y = 0
        i = 0
        while i < 48:
            self.rect.center = (640, y)
            pygame.draw.rect(self.screen, self.bounary_color, self.rect)
            y += 15
            i += 1
            self.rect.center = (640, y)
            pygame.draw.rect(self.screen, self.boundary_color_two, self.rect)
            y += 15
            i += 1

