import pygame
from pygame.sprite import Sprite


class TurretOne(Sprite):

    def __init__(self, ap_game):
        super().__init__()
        self.screen = ap_game.screen
        self.screen_rect = ap_game.screen.get_rect()
        self.turret_health = 5

        # the first turret
        self.image = pygame.image.load("turret.png")
        self.rect = self.image.get_rect()
        self.rect.center = (960, 80)

        # Store decimal value for ship's horizontal and vertical position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y
        if self.turret_health < 5:
            self.image = pygame.image.load("hurt_turret.png")


class TurretTwo(Sprite):

    def __init__(self, ap_game):
        super().__init__()
        self.screen = ap_game.screen
        self.screen_rect = ap_game.screen.get_rect()
        self.turret_health = 100

        # the first turret
        self.image = pygame.image.load("turret.png")
        self.rect = self.image.get_rect()
        self.rect.center = (870, 320)

        # Store decimal value for ship's horizontal and vertical position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y
        if self.turret_health < 5:
            self.image = pygame.image.load("hurt_turret.png")


class TurretThree(Sprite):

    def __init__(self, ap_game):
        super().__init__()
        self.screen = ap_game.screen
        self.screen_rect = ap_game.screen.get_rect()
        self.turret_health = 100

        # the first turret
        self.image = pygame.image.load("turret.png")
        self.rect = self.image.get_rect()
        self.rect.center = (960, 560)

        # Store decimal value for ship's horizontal and vertical position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y
        if self.turret_health < 5:
            self.image = pygame.image.load("hurt_turret.png")


