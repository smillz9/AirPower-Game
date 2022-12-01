import time

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
from turret_bullets import TurretOneBullet
from turret_bullets import TurretTwoBullet
from turret_bullets import TurretThreeBullet
from gameover import GameOver


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

        self.ship = Ship(self)
        self.ship_two = ShipTwo(self)

        self.turret_one = Turret(self, (960, 80))
        self.turret_two = Turret(self, (870, 320))
        self.turret_three = Turret(self, (960, 560))

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
        self.turrets.add([self.turret_one, self.turret_two, self.turret_three])

        self.bullets = pygame.sprite.Group()
        self.ship_bullet = ShipBullet(self)

        self.ship_two_bullets = pygame.sprite.Group()
        self.ship_two_bullet = ShipTwoBullet(self)

        self.turret_three_bullet = TurretThreeBullet(self)
        self.turret_two_bullet = TurretTwoBullet(self)
        self.turret_one_bullet = TurretOneBullet(self)

        self.turret_bullets = pygame.sprite.Group()
        self.turret_two_bullets = pygame.sprite.Group()
        self.turret_three_bullets = pygame.sprite.Group()

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

    def fire_turretone_bullet(self):
        if len(self.turret_bullets) < 1:
            new_turret_bullet_one = TurretOneBullet(self)
            self.turret_bullets.add(new_turret_bullet_one)

    def update_turretone_bullets(self):
        self.turret_bullets.update()
        for bullet in self.turret_bullets.copy():
            if bullet.rect.right <= self.screen.get_rect().left:
                self.turret_bullets.remove(bullet)
        if self.turret_one in self.turrets:
            self.fire_turretone_bullet()

        self.bullet_ship_collision()
        self.turret_bullet_homehangar_collision()

    def fire_turrettwo_bullet(self):
        if len(self.turret_two_bullets) < 1:
            new_turret_bullet_two = TurretTwoBullet(self)
            self.turret_two_bullets.add(new_turret_bullet_two)

    def update_turrettwo_bullets(self):
        self.turret_two_bullets.update()
        for bullet in self.turret_two_bullets.copy():
            if bullet.rect.right <= self.screen.get_rect().left:
                self.turret_two_bullets.remove(bullet)
        if self.turret_two in self.turrets:
            self.fire_turrettwo_bullet()

        self.bullet_ship_collision()
        self.turret_bullet_homehangar_collision()

    def fire_turretthree_bullet(self):
        if len(self.turret_three_bullets) < 1:
            new_turret_bullet_three = TurretThreeBullet(self)
            self.turret_three_bullets.add(new_turret_bullet_three)

    def update_turretthree_bullets(self):
        self.turret_three_bullets.update()
        for bullet in self.turret_three_bullets.copy():
            if bullet.rect.right <= self.screen.get_rect().left:
                self.turret_three_bullets.remove(bullet)
        if self.turret_three in self.turrets:
            self.fire_turretthree_bullet()

        self.bullet_ship_collision()
        self.turret_bullet_homehangar_collision()
    def run_game(self):
        # while loop is used for updating positions of
        clock = pygame.time.Clock()
        while True:

            self._check_events()

            self.update_bullets()
            self.update_shiptwo_bullets()
            self.update_turretone_bullets()
            self.update_turrettwo_bullets()
            self.update_turretthree_bullets()

            self.gameobjects.update()
            self.turrets.update()

            # self.draw_background()
            self.screen.fill((119, 190, 220))
            self.home_island.blitme()  # create an island surface
            self.enemy_island.blitme()  # create enemy island
            self.gameobjects.draw(self.screen)
            if self.enemy_hangar in self.enemy_base:
                self.enemy_base.draw(self.screen)
            self.turrets.draw(self.screen)
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            for bullet in self.ship_two_bullets.sprites():
                bullet.draw_bullet()
            for bullet in self.turret_bullets.sprites():
                bullet.draw_bullet()
            if self.ship not in self.player_one and self.ship_two not in self.player_two:
                self.end.display_lose_message()
            if self.home_hangar not in self.gameobjects:
                self.end.display_lose_message()
            if self.enemy_hangar not in self.enemy_base:
                self.end.display_win_message()
            pygame.display.flip()

            clock.tick(60)

            # the brains of the game


if __name__ == '__main__':
    # make game instance and run it
    ap = AirPower()
    ap.run_game()
