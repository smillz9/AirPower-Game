import pygame


class GameOver:
    """a class to initialize the final screen"""
    def __init__(self, ap_game):
        pygame.init()
        # settings for final message
        self.screen = ap_game.screen
        self.screen_rect = self.screen.get_rect()
        lose_message = "You Lose"
        win_message = "You Win"
        self.text_color = (250, 250, 250)
        self.bg_color = (0, 0, 0)

        # create components of final message
        self.font = pygame.font.SysFont('monospace', 100, bold=True, italic=False)
        self.lose_image = self.font.render(lose_message, True, self.text_color, self.bg_color)
        self.win_image = self.font.render(win_message, True, self.text_color, self.bg_color)
        self.text_rect = self.lose_image.get_rect()
        self.text_rect.center = self.screen_rect.center

    def display_lose_message(self):
        # display final message on top of a new background
        self.screen.fill((173, 3, 46))
        self.screen.blit(self.lose_image, self.text_rect)

    def display_win_message(self):
        self.screen.fill((28, 189, 44))
        self.screen.blit(self.win_image, self.text_rect)
