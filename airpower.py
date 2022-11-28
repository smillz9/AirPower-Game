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
from turret import TurretOne
from turret import TurretTwo
from turret import TurretThree
from turret_bullets import TurretOneBullet


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

        #self.num_tiles = self.screen_rect.width // self.water_rect.width

        self.ship = Ship(self)
        self.ship_two = ShipTwo(self)

        self.turret_one = TurretOne(self)
        self.turret_two = TurretTwo(self)
        self.turret_three = TurretThree(self)

        self.home_island = HomeIsland(self) # create home island instance
        self.home_island.move((256, 320))  # set location for home island

        self.enemy_island = EnemyIsland(self) # create enemy island instance
        self.enemy_island.move((960, 320))  # set location for enemy island

        self.home_hangar = HomeHangar(self) # create home hangar instance
        self.enemy_hangar = EnemyHangar(self) # create enemy hangar instance

        # Sprite group for home hangar, ship, enemy hangar
        self.gameobjects = pygame.sprite.Group()
        self.gameobjects.add([self.home_hangar, self.enemy_hangar, self.ship, self.ship_two])

        self.enemy_base = pygame.sprite.Group()
        self.enemy_base.add([self.enemy_hangar])

        # Sprite group for the turrets
        self.turrets = pygame.sprite.Group()
        self.turrets.add([self.turret_one, self.turret_two, self.turret_three])

        self.bullets = pygame.sprite.Group()
        self.ship_bullet = ShipBullet(self)

        self.ship_two_bullets = pygame.sprite.Group()
        self.ship_two_bullet = ShipTwoBullet(self)

        self.turret_one_bullet = TurretOneBullet(self)
        self.turret_bullets = pygame.sprite.Group()

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
        collisions = pygame.sprite.groupcollide(self.bullets, self.turrets, True, True)
        #print(f"{self.turret_one.turret_health}")

        if collisions:
            for turrets in collisions.values():
                if turrets == self.turret_one:
                    if self.turret_one.turret_health > 0:
                        self.turret_one.turret_health -= 1
                    elif self.turret_one.turret_health == 1:
                        self.turrets.remove(self.turret_one)
                if turrets == self.turret_two:
                    self.turrets.remove(self.turret_two)
                if turrets == self.turret_three:
                    self.turrets.remove(self.turret_three)

    def bullet_enemyhangar_collision(self):
        """respond to when bullets hit enemy hangar"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.enemy_base, True, True)

        if collisions:
            for x in collisions.values():
                if x == self.enemy_base:
                    if self.enemy_hangar.health > 1:
                        self.enemy_hangar.health -= 1
                    else:
                        self.enemy_base.remove(self.enemy_hangar)
    def fire_bullet(self):
        """create bullets and add it to group"""
        if len(self.bullets) < 6:
            new_bullet = ShipBullet(self)
            self.bullets.add(new_bullet)
    def fire_bullet_two(self):
        if len(self.ship_two_bullets) < 6:
            another_bullet = ShipTwoBullet(self)
            self.ship_two_bullets.add(another_bullet)

    #def draw_background(self):
        #for y in range(self.num_tiles):
            #for x in range(self.num_tiles):
                #self.screen.blit(self.water, (x * self.water_rect.width, y * self.water_rect.height))

    def update_bullets(self):
        """update positions of bullets and get rid of old bullets"""
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.screen.get_rect().right:
                self.bullets.remove(bullet)

        self.bullet_turret_collision()
        self.bullet_enemyhangar_collision()

    def update_shiptwo_bullets(self):
        self.ship_two_bullets.update()
        for bullet in self.ship_two_bullets.copy():
            if bullet.rect.left >= self.screen.get_rect().right:
                self.ship_two_bullets.remove(bullet)

    def fire_turret_bullet(self):
        if len(self.turret_bullets) < 6:
            new_turret_bullet = TurretOneBullet(self)
            self.turret_bullets.add(new_turret_bullet)

    def update_turret_bullets(self):
        self.fire_turret_bullet()
        self.turret_bullets.update()
        for bullet in self.turret_bullets.copy():
            if bullet.rect.right <= self.screen.get_rect().left:
                self.turret_bullets.remove(bullet)
        time.sleep(3)

    def run_game(self):
        # while loop is used for updating positions of
        clock = pygame.time.Clock()
        while True:

            self._check_events()

            self.update_bullets()
            self.update_shiptwo_bullets()
            #self.update_turret_bullets()

            self.gameobjects.update()
            self.turrets.update()

            #self.draw_background()
            self.screen.fill((119, 190, 220))
            self.home_island.blitme()  # create an island surface
            self.enemy_island.blitme()  # create enemy island
            self.gameobjects.draw(self.screen)
            self.turrets.draw(self.screen)
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            for bullet in self.ship_two_bullets.sprites():
                bullet.draw_bullet()

            pygame.display.flip()

            clock.tick(60)

            # the brains of the game


if __name__ == '__main__':
    # make game instance and run it
    ai = AirPower()
    ai.run_game()
