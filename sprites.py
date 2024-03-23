import pygame as pg
from settings import *

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE * 0.75, TILESIZE * 0.75))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y
        self.moneybag = 0
        self.speed_boost_active = False
        self.speed_boost_end_time = 0

    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        speed = BOOSTED_PLAYER_SPEED if self.speed_boost_active else PLAYER_SPEED
        if keys[pg.K_LEFT] or keys[pg.K_a]: self.vx = -speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]: self.vx = speed
        if keys[pg.K_UP] or keys[pg.K_w]: self.vy = -speed
        if keys[pg.K_DOWN] or keys[pg.K_s]: self.vy = speed
        if self.vx != 0 and self.vy != 0:  # Diagonal movement
            self.vx *= 0.7071
            self.vy *= 0.7071

    def update(self):
        self.get_keys()
        self.rect.x += self.vx * self.game.dt
        self.collide_with_walls('x')
        self.rect.y += self.vy * self.game.dt
        self.collide_with_walls('y')
        if self.speed_boost_active and pg.time.get_ticks() > self.speed_boost_end_time:
            self.speed_boost_active = False
            self.vx, self.vy = PLAYER_SPEED, PLAYER_SPEED  # Reset speed to normal
        self.collide_with_coins()
        self.collide_with_speed_boosts()

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
        hits = pg.sprite.spritecollide(self, self.game.coins, True)
        for hit in hits:
            self.moneybag += 1  # Or however you want to handle coin collection

    def collide_with_speed_boosts(self):
        hits = pg.sprite.spritecollide(self, self.game.speed_boosts, True)
        for hit in hits:
            self.speed_boost_active = True
            self.speed_boost_end_time = pg.time.get_ticks() + 10000  # 10 seconds of boost

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