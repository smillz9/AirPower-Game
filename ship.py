import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.health = 100
        self.healthy_image = pygame.image.load("navy_ship.png")

        self.image = self.healthy_image
        self.rect = self.image.get_rect()

    def move(self, coordinate):
        self.rect.center = coordinate

    def blitme(self):
        #if self.health < 40:
            #self.image =
        self.screen.blit(self.image, self.rect)