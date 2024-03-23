import pygame as pg
import sys
from os import path
from settings import *
from sprites import Player, Wall, Coin, SpeedBoost

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()
        self.font = pg.font.Font(pg.font.match_font('arial'), 22)

    def load_data(self):
        self.map_data = []
        game_folder = path.dirname(__file__)
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line.strip())

    def new(self):
        # Reset the game setup
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.speed_boosts = pg.sprite.Group()
        self.start_time = 60  # Timer reset for each new game
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

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
            if self.start_time <= 0:
                print("Time's up! Game over.")
                self.playing = False

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()
        self.start_time -= self.dt  # Decrement the timer by the elapsed time

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (HEIGHT, y))

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        # Timer display
        timer_text = f"Time: {int(self.start_time)}"
        text_surface = self.font.render(timer_text, True, WHITE)
        text_rect = text_surface.get_rect(midtop=(WIDTH / 2, 10))
        self.screen.blit(text_surface, text_rect)
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

if __name__ == '__main__':
    g = Game()
    g.new()  # Prepare a new game
    g.run()  # Start the main game loop