# This file was created by Liam Luinenburg (and AI)
import pygame as pg
from settings import *

# Define the Player class
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE * 0.75, TILESIZE * 0.75))
        self.image.fill(GREEN)
        self.original_image = self.image.copy()  # Keep an original copy for fading
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y
        self.fading = None  # 'in', 'out', or None
        self.fade_counter = 255  # Start fully opaque
        self.destination_portal = None
        self.last_portal_use_time = 0  # Track the last time a portal was used
        self.speed_boost_active = False  # Initialize speed boost active status
        self.speed_boost_end_time = 0  # Initialize speed boost end time
        self.moneybag = 0  # Initialize coin collection count

    def get_keys(self):
        if self.fading is None:  # Only move if not currently fading
            self.vx, self.vy = 0, 0
            keys = pg.key.get_pressed()
            speed = BOOSTED_PLAYER_SPEED if self.speed_boost_active else PLAYER_SPEED
            if keys[pg.K_LEFT] or keys[pg.K_a]: self.vx = -speed
            if keys[pg.K_RIGHT] or keys[pg.K_d]: self.vx = speed
            if keys[pg.K_UP] or keys[pg.K_w]: self.vy = -speed
            if keys[pg.K_DOWN] or keys[pg.K_s]: self.vy = speed
            if self.vx != 0 and self.vy != 0:
                self.vx *= 0.7071
                self.vy *= 0.7071

    def update(self):
        if self.fading is None:
            self.get_keys()
            self.rect.x += self.vx * self.game.dt
            self.collide_with_walls('x')
            self.rect.y += self.vy * self.game.dt
            self.collide_with_walls('y')
            self.collide_with_coins()
        if self.fading is None or self.fading == 'in':
            self.collide_with_portals()
        self.handle_fading()

    def handle_fading(self):
        if self.fading == 'out' and self.fade_counter > 0:
            self.fade_counter -= 15
            self.image.set_alpha(self.fade_counter)
            if self.fade_counter <= 0:
                self.teleport_to_portal()
        elif self.fading == 'in' and self.fade_counter < 255:
            self.fade_counter += 15
            self.image.set_alpha(self.fade_counter)
            if self.fade_counter >= 255:
                self.fading = None

    def teleport_to_portal(self):
        if self.destination_portal:
            self.rect.x = self.destination_portal.rect.x
            self.rect.y = self.destination_portal.rect.y
            self.fading = 'in'
            self.destination_portal = None

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0: self.rect.right = hits[0].rect.left
                if self.vx < 0: self.rect.left = hits[0].rect.right
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0: self.rect.bottom = hits[0].rect.top
                if self.vy < 0: self.rect.top = hits[0].rect.bottom

    def collide_with_coins(self):
        hits = pg.sprite.spritecollide(self, self.game.coins, True)  # True to kill the coin sprite
        for hit in hits:
            self.moneybag += 1  # Update player's coin count or similar attribute

    def collide_with_portals(self):
        current_time = pg.time.get_ticks()
        if current_time - self.last_portal_use_time > 3000 and self.fading is None:  # 3000 ms = 3 seconds cooldown
            hits = pg.sprite.spritecollide(self, self.game.portals, False)
            if hits:
                self.fading = 'out'
                self.destination_portal = self.find_destination_portal(hits[0])
                self.last_portal_use_time = current_time  # Update last use time

    def find_destination_portal(self, entry_portal):
        for portal in self.game.portals:
            if portal != entry_portal and portal.color == entry_portal.color:
                return portal
        return entry_portal  # Fallback to the original portal if no match found

# Define the Wall class
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y

# Define the Coin class
class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y

# Define the SpeedBoost class
class SpeedBoost(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.speed_boosts
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y

# Define the Portal class
class Portal(pg.sprite.Sprite):
    def __init__(self, game, x, y, color):
        self.groups = game.all_sprites, game.portals
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.color = color
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y