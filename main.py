# This file was created by Liam Luinenburg (and AI)

# Design Goals:
# 1. Create speedboost power up
# 2. Create coin collection system
# 3. Create game countdown timer
# 4. Create win/lose system

# Beta Goal: Make different levels

# Import necessary libraries
import pygame as pg
import sys
from os import path
from settings import *  # Import game settings
from sprites import Player, Wall, Coin, SpeedBoost  # Import sprite classes

class Game:
    # Initialize the game
    def __init__(self):
        pg.init()  # Initialize Pygame
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))  # Set up the display
        pg.display.set_caption(TITLE)  # Set the window title
        self.clock = pg.time.Clock()  # Set up a clock
        self.level = 1  # Current level
        self.load_data(self.level)  # Load data for the first level
        self.font = pg.font.Font(pg.font.match_font('arial'), 22)  # Font for displaying text
        self.win = False  # Check if the player has won

    # Load data from files, now supports multiple levels
    def load_data(self, level):
        self.map_data = []  # Initialize an empty list for map data
        game_folder = path.dirname(__file__)
        # Correct map file handling for the first level and beyond
        map_file = 'map.txt' if level == 1 else f'map{level}.txt'
        with open(path.join(game_folder, map_file), 'rt') as f:
            for line in f:
                self.map_data.append(line.strip())

    # Set up a new game, now depends on the level
    def new(self):
        # Initialize sprite groups
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.speed_boosts = pg.sprite.Group()
        self.start_time = 60  # Reset the timer for the new game
        
        # Create sprites based on the map data
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                elif tile == 'P':
                    self.player = Player(self, col, row)
                elif tile == 'C':
                    Coin(self, col, row)
                elif tile == 'S':
                    SpeedBoost(self, col, row)

    # Main game loop, now handles level transitions
    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000  # Control game speed
            self.events()
            self.update()
            self.draw()
            if self.start_time <= 0:
                print("Time's up! Game over.")
                self.playing = False
            if self.win:
                if self.level < 3:  # Updated to handle three levels
                    self.level += 1
                    self.load_data(self.level)  # Load next level
                    self.new()
                    self.win = False
                else:
                    break

    # Quit the game
    def quit(self):
        pg.quit()
        sys.exit()

    # Update game state, now includes level handling
    def update(self):
        self.all_sprites.update()  # Update all sprites
        self.start_time -= self.dt  # Update the timer
        
        # Check if all coins are collected
        if len(self.coins) == 0 and not self.win:
            self.win = True
            self.display_win_message()
            pg.time.wait(2000)  # Wait for 2 seconds before closing
            if self.level == 3:
                self.quit()

    # Draw the grid background
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (HEIGHT, y))

    # Draw all game elements
    def draw(self):
        self.screen.fill(BLACK)  # Fill screen with black
        self.draw_grid()  # Draw the grid
        self.all_sprites.draw(self.screen)  # Draw all sprites
        
        # Draw the timer unless win message is being displayed
        if not self.win:
            timer_text = f"Time: {int(self.start_time)}"
            text_surface = self.font.render(timer_text, True, WHITE)
            text_rect = text_surface.get_rect(midtop=(WIDTH / 2, 10))
            self.screen.blit(text_surface, text_rect)
        pg.display.flip()  # Update the display

    # Handle input and window events
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

    # Display win message
    def display_win_message(self):  # Corrected syntax here
        self.screen.fill(BLACK)  # Clear the screen
        win_text = "Level Complete!" if self.level < 3 else "You Win!"
        text_surface = self.font.render(win_text, True, WHITE)  # Render the win text
        text_rect = text_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2))  # Position the text
        self.screen.blit(text_surface, text_rect)  # Draw the text on the screen
        pg.display.flip()  # Update the display to show the text

if __name__ == '__main__':
    g = Game()
    g.new()  # Set up a new game
    g.run()  # Start the main game loop