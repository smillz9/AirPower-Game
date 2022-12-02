import pygame.font
import time
from pygame.sprite import Group

class Score:
    """a class that manages the text on the screen"""

    def __init__(self, ap_game):
        self.screen = ap_game.screen
        self.screen_rect = self.screen.get_rect()

        self.text_color = (250, 250, 250)
        self.bg_color = (0, 0, 0)
        self.x = 0
        time = round(self.x, 0)
        time_str = "{:,}".format(time)
        # create components of final message
        self.font = pygame.font.SysFont('monospace', 50, bold=True, italic=False)
        self.timer_image = self.font.render(time_str, True, self.text_color, self.bg_color)
        self.text_rect = self.timer_image.get_rect()
        self.text_rect.center = (100,30)

    def display_time(self):
        self.screen.blit(self.timer_image, self.text_rect)
        self.x += 1
        time.sleep(1)
