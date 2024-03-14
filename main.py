# This file was created by: Liam Luinenburg

# import libraries and modules
import pygame as pg
from settings import *
from sprites import *
from random import randint
import sys
from os import path

# Define game class...
class Game:
    # Define a special method to init the properties of said class...
    def __init__(self):
        # init pygame
        pg.init()
        # set size of screen and be the screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # setting game clock 
        self.clock = pg.time.Clock()
        self.load_data()
        self.start_time = 10  # Timer starting from 10 seconds

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
        
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)

    # Create run method which runs the whole GAME
    def new(self):
        print("create new game...")
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

            # Check for win condition
            if not self.coins and self.start_time > 0:
                print("You win!")
                self.playing = False
            elif self.start_time <= 0:
                print("You lose! Time's up!")
                self.playing = False

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()
        # Update the timer
        if self.start_time > 0:
            self.start_time -= self.dt
        else:
            self.playing = False  # Stop the game when the timer reaches 0

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x * TILESIZE, y * TILESIZE)
        surface.blit(text_surface, text_rect)

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        # Display timer
        self.draw_text(self.screen, "Time: {:.2f}".format(self.start_time), 22, WHITE, 0, 0)
        self.draw_text(self.screen, str(self.player.moneybag), 64, WHITE, 1, 1)

        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

# Instantiate the game... 
g = Game()
# use game method run to run
while True:
    g.new()
    g.run()