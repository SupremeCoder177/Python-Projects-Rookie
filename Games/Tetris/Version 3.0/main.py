import pygame as pg
import os
from sys import exit
from json import load
from widgets import Button
from blocky import Blocky



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
        self.clock = pg.time.Clock()

        self.font = pg.font.Font("Fonts/StayPixel.ttf", self.settings["font_size"])
        self.frames_elapsed = 0

        # the cute screen pet LOL 
        self.blocky = Blocky(self, self.settings["blocky_pos"][0], self.settings["blocky_pos"][1], int(self.settings["tile_size"] * 2.5))

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

            # drawing blocky
            self.blocky.draw()

            pg.display.update()
            self.clock.tick(self.settings["fps"])
        exit()


if __name__ == "__main__":
    g = Game()
    g.run()