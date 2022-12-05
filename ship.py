import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, ap_game):
        super().__init__()
        self.screen = ap_game.screen
        self.screen_rect = ap_game.screen.get_rect()
        self.health = 10
        self.ship_speed = 15
        self.healthy_image = pygame.image.load("new_player_one.png")

        self.image = self.healthy_image
        self.rect = self.image.get_rect()


        # Store decimal value for ship's horizontal and vertical position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # movement flags
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right/2:
            self.x += self.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.ship_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.ship_speed
        if self.moving_down and self.rect.bottom <= self.screen_rect.bottom:
            self.y += self.ship_speed

        self.rect.x = self.x
        self.rect.y = self.y
