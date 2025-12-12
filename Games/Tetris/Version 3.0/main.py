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

        # the cute (kinda) screen pet LOL 
        self.blocky = Blocky(self, self.settings["blocky_pos"][0], self.settings["blocky_pos"][1], int(self.settings["tile_size"] * 2.5), self.font, "black")

        self.falling_brick = Brick(self)

        self.frame_cap = 10e4

        # the bricks on screen animations
        self.anims = [BrickFactory().get_animation(color) for color in BrickFactory().get_all_colors()]
        self.coor_map = dict()

    # the main game loop
    def run(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    running = False
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_k:
                        self.blocky.send_message("Hello I am blocky, your personal screen companion.", 5)
                        self.blocky.set_state("spin")

            # updating frames elapsed
            self.frames_elapsed += 1
            self.frames_elapsed %= self.frame_cap

            # clearing the screen
            self.screen.fill((30, 30, 30)) # gray

            self.draw_grid("#000000", "#333333") # a black grid with gray borders

            # updating and drawing the falling brick
            self.falling_brick.update()
            self.falling_brick.draw(self.screen)

            # updating brick animation
            for i in range(len(self.anims)):
                self.anims[i].update(self.frames_elapsed)

            # drawing the bricks
            for coor in self.coor_map.keys():
                self.anims[self.coor_map[coor]].draw(coor[0] + self.settings["grid_pos"][0], coor[1] + self.settings["grid_pos"][1], self.screen, self.settings["tile_size"])

            # drawing blocky
            self.blocky.draw()                
 
            pg.display.update()
            self.clock.tick(self.settings["fps"])
        exit()

    # draws a grid on the screen of the given color
    def draw_grid(self, color : str, grid_color : str):
        for i in range(self.settings["grid_size"][0] // self.settings["tile_size"]):
            for j in range(self.settings["grid_size"][1] // self.settings["tile_size"]):
                pg.draw.rect(self.screen, color, (i * self.settings["tile_size"] + self.settings["grid_pos"][0], j * self.settings["tile_size"] + self.settings["grid_pos"][1], self.settings["tile_size"], self.settings["tile_size"]))
                pg.draw.rect(self.screen, grid_color, (i * self.settings["tile_size"] + self.settings["grid_pos"][0], j * self.settings["tile_size"] + self.settings["grid_pos"][1], self.settings["tile_size"], self.settings["tile_size"]), 1)

    # adding bricks on the screen
    def add_brick(self, coors : List[int], color : str):
        for i in range(len(self.anims)):
            if self.anims[i] == BrickFactory().get_animation(color):
                for coor in coors:
                    self.coor_map[coor] = i

        # after adding a brick, we check if it completed any lines
        self.check_lines()

    # checks and removes and updates block positions for all the lines which are completed
    def check_lines(self):
        while True:
            y = self.check_line_completion()
            if not y: break

            # removing the coordinates from the coor_map
            for x in range(self.settings["grid_size"][0] // self.settings["tile_size"]):
                del self.coor_map[(x * self.settings["tile_size"], y)]

            temp = self.coor_map.copy()
            self.coor_map = dict()

            for key, value in temp.items():
                coor = list(key)
                if coor[1] < y:
                    coor[1] += self.settings["tile_size"]
                self.coor_map[tuple(coor)] = value

    # checking if a line has been completed, starting from the top
    def check_line_completion(self):
        for y in range(self.settings["grid_size"][1] // self.settings["tile_size"]):
            complete = True
            for x in range(self.settings["grid_size"][0] // self.settings["tile_size"]):
                if self.coor_map.get((x * self.settings["tile_size"], y * self.settings["tile_size"]), -1) < 0:
                    complete = False
                    break
            if complete:
                return y * self.settings["tile_size"]
        return None

if __name__ == "__main__":
    g = Game()
    g.run()