import pygame
import sys
from ship import Ship


class AirPower:
    def __init__(self):
        pygame.init()
        self.TILE_SIZE = 64
        self.WINDOW_SIZE = 10 * self.TILE_SIZE

        self.screen = pygame.display.set_mode((self.WINDOW_SIZE * 2, self.WINDOW_SIZE))
        self.water = pygame.image.load("water.png")
        self.water_rect = self.water.get_rect()
        self.screen_rect = self.screen.get_rect()

        self.num_tiles = self.screen_rect.width // self.water_rect.width

        self.ship = Ship(self)


    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                coordinate = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("BOOM")

    def draw_background(self):
        for y in range(self.num_tiles):
            for x in range(self.num_tiles):
                self.screen.blit(self.water, (x * self.water_rect.width, y * self.water_rect.height))

    def _update_screen(self):
        self.draw_background()
        self.ship.blitme()
        pygame.display.flip()

    def run_game(self):
        while True:
            self._check_events()
            self._update_screen()
            # the brains of the game


if __name__ == '__main__':
    # make game instance and run it
    ai = AirPower()
    ai.run_game()
