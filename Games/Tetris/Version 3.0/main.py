import pygame as pg
import os
from typing import List
from sys import exit
from json import load
from widgets import Button
from blocky import Blocky
from bricks import Brick
from bricks import BrickFactory


# main game class
class Game:

    def __init__(self):
        if not "settings.json" in os.listdir():
            print("Settings not found in current working directory, exiting...")
            exit()

        with open("settings.json", "r") as f:
            self.settings = load(f)

        pg.init()
        self.screen = pg.display.set_mode(self.settings["window_size"])
        pg.display.set_caption("Tetris Version 3.0")
        self.clock = pg.time.Clock()

        self.font = pg.font.Font("Fonts/StayPixel.ttf", self.settings["font_size"])
        self.frames_elapsed = 0

        # the cute screen pet LOL 
        self.blocky = Blocky(self, self.settings["blocky_pos"][0], self.settings["blocky_pos"][1], int(self.settings["tile_size"] * 2.5))

        self.falling_brick = Brick(self)

        # the bricks on screen animations
        self.anims = [BrickFactory().get_group_animation(color) for color in BrickFactory().get_all_colors()]
        self.coors = [[] for i in range(len(BrickFactory().get_all_colors()))]

    # the main game loop
    def run(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    running = False

            # updating frames elapsed
            self.frames_elapsed += 1
            self.frames_elapsed %= self.settings["fps"]

            # clearing the screen
            self.screen.fill((100, 100, 100)) # black

            self.draw_grid("white")

            # drawing blocky
            self.blocky.draw()

            # updating and drawing the falling brick
            self.falling_brick.update()
            self.falling_brick.draw(self.screen)

            # updating and drawing the bricks on screen
            for i in range(len(self.anims)):
                self.anims[i].update(self.frames_elapsed)
                self.anims[i].draw_coords(self.coors[i], self.screen, self.settings["tile_size"])
 
            pg.display.update()
            self.clock.tick(self.settings["fps"])
        exit()

    # draws a grid on the screen of the given color
    def draw_grid(self, color : str):
        for i in range(self.settings["grid_size"][0] // self.settings["tile_size"]):
            for j in range(self.settings["grid_size"][1] // self.settings["tile_size"]):
                pg.draw.rect(self.screen, color, (i * self.settings["tile_size"] + self.settings["grid_pos"][0], j * self.settings["tile_size"] + self.settings["grid_pos"][1], self.settings["tile_size"], self.settings["tile_size"]), 1)

    def add_brick(self, coors : List[int], color : str):
        for i in range(len(self.anims)):
            if self.anims[i] == BrickFactory().get_animation(color):
                for coor in coors:
                    self.coors[i].append((coor[0] + self.settings["grid_pos"][0], coor[1] + self.settings["grid_pos"][1]))

if __name__ == "__main__":
    g = Game()
    g.run()