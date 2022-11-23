import pygame
import sys
from ship import Ship
from home_island import HomeIsland
from enemy_island import EnemyIsland
from home_hangar import HomeHangar
from enemy_hangar import EnemyHangar
from ship_bullet import ShipBullet
from turret import TurretOne
from turret import TurretTwo
from turret import TurretThree


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

        self.num_tiles = self.screen_rect.width // self.water_rect.width

        self.ship = Ship(self)
        self.turret_one = TurretOne(self)
        self.turret_two = TurretTwo(self)
        self.turret_three = TurretThree(self)

        self.home_island = HomeIsland(self)

        self.home_island.move((256, 320))  # set location for home island

        self.enemy_island = EnemyIsland(self)
        self.enemy_island.move((960, 320))  # set location for enemy island

        self.home_hangar = HomeHangar(self)
        self.enemy_hangar = EnemyHangar(self)

        # Sprite group for home hangar, ship, enemy hangar
        self.gameobjects = pygame.sprite.Group()
        self.gameobjects.add([self.home_hangar, self.enemy_hangar, self.ship])

        # Sprite group for the turrets
        self.turrets = pygame.sprite.Group()
        self.turrets.add(self.turret_one, self.turret_two, self.turret_three)
        self.bullets = pygame.sprite.Group()

        self.ship_bullet = ShipBullet(self)

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

    def bullet_turret_collision(self):
        """respond to when bullets hit the turrets"""
        collisions = pygame.sprite.groupcollide(self.bullets, self.turrets, True, True)

        if collisions:
            for turrets in collisions.values():
                if turrets == self.turret_one:
                    self.turrets.remove(self.turret_one)
                if turrets == self.turret_two:
                    self.turrets.remove(self.turret_two)
                if turrets == self.turret_three:
                    self.turrets.remove(self.turret_three)
    def fire_bullet(self):
        """create bullets and add it to group"""
        if len(self.bullets) < 6:
            new_bullet = ShipBullet(self)
            self.bullets.add(new_bullet)

    def draw_background(self):
        for y in range(self.num_tiles):
            for x in range(self.num_tiles):
                self.screen.blit(self.water, (x * self.water_rect.width, y * self.water_rect.height))

    def update_bullets(self):
        """update positions of bullets and get rid of old bullets"""
        self.bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.left >= self.screen.get_rect().right:
                self.bullets.remove(bullet)

        self.bullet_turret_collision()

    def run_game(self):
        # while loop is used for updating positions of
        clock = pygame.time.Clock()
        while True:

            self._check_events()
          #
            self.update_bullets()

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

            pygame.display.flip()

            clock.tick(60)

            # the brains of the game


if __name__ == '__main__':
    # make game instance and run it
    ai = AirPower()
    ai.run_game()
