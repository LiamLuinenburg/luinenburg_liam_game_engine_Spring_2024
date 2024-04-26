# This file was created by Liam Luinenburg (and AI)
import pygame as pg
from settings import *

from random import randint
from os import path

SPRITESHEET = "theBell.png"
# needed for animated sprite
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'images')



# Define the Player class
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # Initialize the sprite groups
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE * 0.75, TILESIZE * 0.75))  # Create the player image
        self.image.fill(GREEN)  # Color the player image green
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0 
        self.x = x * TILESIZE  # Set the initial x position
        self.y = y * TILESIZE  # Set the initial y position
        self.rect.x = self.x
        self.rect.y = self.y
        self.moneybag = 0
        self.speed_boost_active = False
        self.speed_boost_end_time = 0

    # Handle keyboard input
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()  # Get the state of all keyboard buttons
        speed = BOOSTED_PLAYER_SPEED if self.speed_boost_active else PLAYER_SPEED
        if keys[pg.K_LEFT] or keys[pg.K_a]: self.vx = -speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]: self.vx = speed
        if keys[pg.K_UP] or keys[pg.K_w]: self.vy = -speed
        if keys[pg.K_DOWN] or keys[pg.K_s]: self.vy = speed
        # Adjust for diagonal movement
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    # Update the player's state
    def update(self):
        self.get_keys()
        self.rect.x += self.vx * self.game.dt  # Apply velocity to x position
        self.collide_with_walls('x')  # Check for collisions in x direction
        self.rect.y += self.vy * self.game.dt  # Apply velocity to y position
        self.collide_with_walls('y')  # Check for collisions in y direction
        if self.speed_boost_active and pg.time.get_ticks() > self.speed_boost_end_time:
            self.speed_boost_active = False
            self.vx, self.vy = PLAYER_SPEED, PLAYER_SPEED
        self.collide_with_coins()  # Check for coin collection
        self.collide_with_speed_boosts()  # Check for speed boost collection

    # Handle collisions with walls
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

    # Handle coin collection
    def collide_with_coins(self):
        hits = pg.sprite.spritecollide(self, self.game.coins, True)
        for hit in hits:
            self.moneybag += 1

    # Handle speed boost collection
    def collide_with_speed_boosts(self):
        hits = pg.sprite.spritecollide(self, self.game.speed_boosts, True)
        for hit in hits:
            self.speed_boost_active = True  # Activate the speed boost
            self.speed_boost_end_time = pg.time.get_ticks() + 10000  # Set the boost
# Define the Wall class
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))  # Create the wall image
        self.image.fill(BLUE)  # Color the wall image blue
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE  # Set the x position
        self.y = y * TILESIZE  # Set the y position
        self.rect.x = self.x  # Update the rectangle x position
        self.rect.y = self.y  # Update the rectangle y position

# Define the Coin class
class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))  # Create the coin image
        self.image.fill(YELLOW)  # Color the coin image yellow
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE  # Set the x position
        self.y = y * TILESIZE  # Set the y position
        self.rect.x = self.x  # Update the rectangle x position
        self.rect.y = self.y  # Update the rectangle y position

# Define the SpeedBoost class
class SpeedBoost(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.speed_boosts
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)  # Color the speed boost image red
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE  # Set the x position
        self.y = y * TILESIZE  # Set the y position
        self.rect.x = self.x  # Update the rectangle x position
        self.rect.y = self.y  # Update the rectangle y position