import time
import random
import pygame
import sys
from ship import Ship
from ship_two import ShipTwo
from home_island import HomeIsland
from enemy_island import EnemyIsland
from home_hangar import HomeHangar
from enemy_hangar import EnemyHangar
from ship_bullet import ShipBullet
from ship_two_bullet import ShipTwoBullet
from turret import Turret
from turret_bullets import TurretBullet
from gameover import GameOver
from pygame import mixer
from scoreboard import Score

# Received assistance from Riley Haugen for music creation
mixer.init()
mixer.music.set_volume(0.8)
mixer.music.load('jazzyfrenchy.mp3')
mixer.music.play()


class AirPower:
    def __init__(self):
        pygame.init()
        # total size of screen: 1280x640
        self.TILE_SIZE = 64
        self.WINDOW_SIZE = 10 * self.TILE_SIZE

        self.screen = pygame.display.set_mode((self.WINDOW_SIZE * 2, self.WINDOW_SIZE))
        self.water = pygame.image.load("water.png")
        self.water_rect = self.water.get_rect()
        self.screen_rect = self.screen.get_rect()
        self.end = GameOver(self)
        self.score = Score(self)

        self.ship = Ship(self)
        self.ship_two = ShipTwo(self)

        self.turret_one = Turret((960, 80))
        self.turret_two = Turret((870, 320))
        self.turret_three = Turret((960, 530))
        self.turret_four = Turret((1000, 100))
        self.turret_five = Turret((900, 250))
        self.turret_six = Turret((900, 480))

        self.home_island = HomeIsland(self)  # create home island instance
        self.home_island.move((256, 320))  # set location for home island

        self.enemy_island = EnemyIsland(self)  # create enemy island instance
        self.enemy_island.move((960, 320))  # set location for enemy island

        self.home_hangar = HomeHangar(self)  # create home hangar instance
        self.enemy_hangar = EnemyHangar(self)  # create enemy hangar instance

        # Sprite group for home hangar, ship, enemy hangar
        self.gameobjects = pygame.sprite.Group()
        self.gameobjects.add([self.home_hangar, self.ship, self.ship_two])

        self.enemy_base = pygame.sprite.Group()
        self.enemy_base.add([self.enemy_hangar])

        self.home_base = pygame.sprite.Group()
        self.home_base.add([self.home_hangar])

        self.player_one = pygame.sprite.Group()
        self.player_one.add([self.ship])

        self.player_two = pygame.sprite.Group()
        self.player_two.add([self.ship_two])
        # Sprite group for the turrets
        self.turrets = pygame.sprite.Group()
        self.turrets.add(
            [self.turret_one, self.turret_two, self.turret_three, self.turret_four, self.turret_five, self.turret_six])

        self.bullets = pygame.sprite.Group()
        self.ship_bullet = ShipBullet(self)

        self.ship_two_bullets = pygame.sprite.Group()
        self.ship_two_bullet = ShipTwoBullet(self)

        self.turret_bullets = pygame.sprite.Group()

        game_title = "Air Power"
        text_color = (250, 250, 250)
        bg_color = (0, 0, 0)

        self.font = pygame.font.SysFont('monospace', 40, bold=True, italic=False)
        self.title_image = self.font.render(game_title, True, text_color, bg_color)
        self.title_rect = self.title_image.get_rect()
        self.title_rect.center = (640, 30)

    def show_shipone_health(self, health):
        self.font_two = pygame.font.SysFont('monospace', 20, bold=True, italic=False)
        self.txt = f"Player One Health: {health}"
        self.screen_txt = self.font_two.render(self.txt, True, [255, 255, 255], [0, 0, 0])
        self.screen.blit(self.screen_txt, [20, 600])

    def show_shiptwo_health(self, health):
        self.font_two = pygame.font.SysFont('monospace', 20, bold=True, italic=False)
        self.txt = f"Player Two Health: {health}"
        self.screen_txt = self.font_two.render(self.txt, True, [255, 255, 255], [0, 0, 0])
        self.screen.blit(self.screen_txt, [300, 600])

    def show_home_hangar_health(self, health):
        self.font_two = pygame.font.SysFont('monospace', 20, bold=True, italic=False)
        self.txt = f"Home Hangar Health: {health}"
        self.screen_txt = self.font_two.render(self.txt, True, [255, 255, 255], [0, 0, 0])
        self.screen.blit(self.screen_txt, [600, 600])

    def show_enemyhangar_health(self, health):
        self.font_two = pygame.font.SysFont('monospace', 20, bold=True, italic=False)
        self.txt = f"Enemy Hangar Health: {health}"
        self.screen_txt = self.font_two.render(self.txt, True, [255, 255, 255], [0, 0, 0])
        self.screen.blit(self.screen_txt, [900, 600])

    def display_title(self):
        self.screen.blit(self.title_image, self.title_rect)

    def draw_clock(self, seconds):
        self.output_str = f"Time: {seconds}"
        self.win_str = f"You Won In: {seconds} seconds! Can You Do Faster?"
        self.lose_str = f"You Survived {seconds} seconds! Can You Beat That Next Time?"
        txt = self.font.render(self.output_str, True, [255, 255, 255])
        self.win_txt = self.font.render(self.win_str, True, [0, 0, 0])
        self.lose_txt = self.font.render(self.lose_str, True, [0, 0, 0])
        self.screen.blit(txt, [50, 30])

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                coordinate = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("BOOM")
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """respond to key presses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            if self.ship in self.player_one:
                self.fire_bullet()
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
        elif event.key == pygame.K_d:
            self.ship_two.moving_right = True
        elif event.key == pygame.K_a:
            self.ship_two.moving_left = True
        elif event.key == pygame.K_w:
            self.ship_two.moving_up = True
        elif event.key == pygame.K_s:
            self.ship_two.moving_down = True
        elif event.key == pygame.K_TAB:
            self.fire_bullet_two()
            bullet_sound = mixer.Sound('laser.wav')
            bullet_sound.play()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """response to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
        elif event.key == pygame.K_d:
            self.ship_two.moving_right = False
        elif event.key == pygame.K_a:
            self.ship_two.moving_left = False
        elif event.key == pygame.K_w:
            self.ship_two.moving_up = False
        elif event.key == pygame.K_s:
            self.ship_two.moving_down = False

    def bullet_turret_collision(self):
        """respond to when bullets hit the turrets"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.turrets, True, False)
        if len(collisions) > 0:
            print(collisions)
            hit_turrets = []
            for turret_list in collisions.values():
                hit_turrets += turret_list
            for turret in hit_turrets:
                print(f"Hit {turret}, has {turret.turret_health} health left")
                turret.turret_health -= 1
                if turret.turret_health == 10:
                    # replace image
                    turret.show_damage()
                if turret.turret_health == 0:
                    explosion_sound = mixer.Sound('explosion.wav')
                    explosion_sound.play()
                    self.turrets.remove(turret)

    def bullet_two_turret_collisions(self):
        """respond to when bullets hit the turrets"""
        collisions = pygame.sprite.groupcollide(self.ship_two_bullets, self.turrets, True, False)

        if len(collisions) > 0:
            print(collisions)
            hit_turrets = []
            for turret_list in collisions.values():
                hit_turrets += turret_list
            for turret in hit_turrets:
                print(f"Hit {turret}, has {turret.turret_health} health left")
                turret.turret_health -= 1
                if turret.turret_health == 10:
                    # replace image
                    turret.show_damage()
                if turret.turret_health == 0:
                    explosion_sound = mixer.Sound('explosion.wav')
                    explosion_sound.play()
                    self.turrets.remove(turret)

    def bullet_enemyhangar_collision(self):
        """respond to when bullets hit enemy hangar"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.enemy_base, True, False)

        if len(collisions) > 0:
            print(collisions)
            hit_base = []
            for hits_list in collisions.values():
                hit_base += hits_list
            for x in hit_base:
                x.health -= 1
                if x.health == 10:
                    x.show_damage()
                if x.health == 0:
                    explosion_sound = mixer.Sound('explosion.wav')
                    explosion_sound.play()
                    self.enemy_base.remove(x)

    def bullet_two_enemyhangar_collision(self):
        collisions = pygame.sprite.groupcollide(self.ship_two_bullets, self.enemy_base, True, False)

        if len(collisions) > 0:
            print(collisions)
            hit_base = []
            for hits_list in collisions.values():
                hit_base += hits_list
            for x in hit_base:
                x.health -= 1
                if x.health == 10:
                    x.show_damage()
                if x.health == 0:
                    explosion_sound = mixer.Sound('explosion.wav')
                    explosion_sound.play()
                    self.enemy_base.remove(x)

    def turret_bullet_homehangar_collision(self):
        """respond when turret bullets hit the home hangar"""
        collisions = pygame.sprite.groupcollide(self.turret_bullets, self.home_base, True, False)
        if len(collisions) > 0:
            print(collisions)
            hit_base = []
            for hits_list in collisions.values():
                hit_base += hits_list
            for x in hit_base:
                x.health -= 1
                if x.health == 10:
                    x.show_damage()
                if x.health == 0:
                    explosion_sound = mixer.Sound('explosion.wav')
                    explosion_sound.play()
                    self.home_base.remove(x)
                    self.gameobjects.remove(x)

    def bullet_ship_collision(self):
        collisions = pygame.sprite.groupcollide(self.turret_bullets, self.player_one, True, False)

        if len(collisions) > 0:
            hit_ship = []
            for hits_list in collisions.values():
                hit_ship += hits_list
            for x in hit_ship:
                x.health -= 1
            if x.health == 0:
                explosion_sound = mixer.Sound('explosion.wav')
                explosion_sound.play()
                self.gameobjects.remove(x)
                self.player_one.remove(x)

    def bullet_ship_two_collision(self):
        collisions = pygame.sprite.groupcollide(self.turret_bullets, self.player_two, True, False)

        if len(collisions) > 0:
            hit_ship = []
            for hits_list in collisions.values():
                hit_ship += hits_list
            for x in hit_ship:
                x.health -= 1
            if x.health == 0:
                explosion_sound = mixer.Sound('explosion.wav')
                explosion_sound.play()
                self.gameobjects.remove(x)
                self.player_two.remove(x)

    def fire_bullet(self):
        """create bullets and add it to group"""
        if len(self.bullets) < 6:
            new_bullet = ShipBullet(self)
            self.bullets.add(new_bullet)

    def fire_bullet_two(self):
        if len(self.ship_two_bullets) < 6:
            another_bullet = ShipTwoBullet(self)
            self.ship_two_bullets.add(another_bullet)

    def update_bullets(self):
        """update positions of bullets and get rid of old bullets"""
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.screen.get_rect().right:
                self.bullets.remove(bullet)

        self.bullet_turret_collision()
        self.bullet_enemyhangar_collision()
        self.bullet_ship_two_collision()

    def update_shiptwo_bullets(self):
        self.ship_two_bullets.update()
        for bullet in self.ship_two_bullets.copy():
            if bullet.rect.left >= self.screen.get_rect().right:
                self.ship_two_bullets.remove(bullet)

        self.bullet_two_turret_collisions()
        self.bullet_two_enemyhangar_collision()

    def shoot(self):
        num = random.randint(0, 1000)
        if num < 5:
            for turret in self.turrets:
                if turret == self.turret_one:
                    new_bullet = TurretBullet(turret.rect.midleft, (-0.944, 0.341))
                    self.turret_bullets.add(new_bullet)
        num = random.randint(0, 1000)
        if num < 5:
            for turret in self.turrets:
                if turret == self.turret_two:
                    new_bullet = TurretBullet(turret.rect.midleft, (-1, 0))
                    self.turret_bullets.add(new_bullet)
        num = random.randint(0, 1000)
        if num < 5:
            for turret in self.turrets:
                if turret == self.turret_three:
                    new_bullet = TurretBullet(turret.rect.midleft, (-0.944, -0.331))
                    self.turret_bullets.add(new_bullet)
        num = random.randint(0, 1000)
        if num < 5:
            for turret in self.turrets:
                if turret == self.turret_four:
                    new_bullet = TurretBullet(turret.rect.midleft, (-0.944, 0.331))
                    self.turret_bullets.add(new_bullet)
        num = random.randint(0, 1000)
        if num < 5:
            for turret in self.turrets:
                if turret == self.turret_five:
                    new_bullet = TurretBullet(turret.rect.midleft, (-1, 0))
                    self.turret_bullets.add(new_bullet)
        num = random.randint(0, 1000)
        if num < 5:
            for turret in self.turrets:
                if turret == self.turret_six:
                    new_bullet = TurretBullet(turret.rect.midleft, (-1, 0))
                    self.turret_bullets.add(new_bullet)

    def update_turret_bullets(self):
        self.turret_bullets.update()
        for bullet in self.turret_bullets.copy():
            if bullet.rect.right <= self.screen.get_rect().left:
                self.turret_bullets.remove(bullet)
        self.shoot()

        self.bullet_ship_collision()
        self.turret_bullet_homehangar_collision()

    def run_game(self):
        # while loop is used for updating positions of
        clock = pygame.time.Clock()
        frame_index = 0
        self.over = False
        while True:

            self._check_events()

            self.update_bullets()
            self.update_shiptwo_bullets()
            self.update_turret_bullets()

            self.gameobjects.update()
            self.turrets.update()

            # self.draw_background()
            self.screen.fill((119, 190, 220))
            self.display_title()
            self.draw_clock(frame_index // 60)
            self.show_shipone_health(self.ship.health)
            self.show_shiptwo_health(self.ship_two.health)
            self.show_home_hangar_health(self.home_hangar.health)
            self.show_enemyhangar_health(self.enemy_hangar.health)

            self.home_island.blitme()  # create an island surface
            self.enemy_island.blitme()  # create enemy island
            self.gameobjects.draw(self.screen)
            if self.enemy_hangar in self.enemy_base:
                self.enemy_base.draw(self.screen)
            self.turrets.draw(self.screen)
            self.turret_bullets.draw(self.screen)
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            for bullet in self.ship_two_bullets.sprites():
                bullet.draw_bullet()
            for bullet in self.turret_bullets.sprites():
                bullet.draw(self.screen)
            if self.ship not in self.player_one and self.ship_two not in self.player_two:
                self.end.display_lose_message()
                self.over = True
                self.screen.blit(self.lose_txt, [10, 30])
            if self.home_hangar not in self.gameobjects:
                self.end.display_lose_message()
                self.over = True
                self.screen.blit(self.lose_txt, [10, 30])
            if self.enemy_hangar not in self.enemy_base:
                self.end.display_win_message()
                self.over = True
                self.screen.blit(self.win_txt, [100, 30])
            pygame.display.flip()

            clock.tick(60)
            if not self.over:
                frame_index += 1

            # the brains of the game


if __name__ == '__main__':
    # make game instance and run it
    ap = AirPower()
    ap.run_game()
