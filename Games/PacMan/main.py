# Making Pac-Man in pygame

import pygame as pg
from graphicsLoader import Load
from sys import exit
from settings import *

class Game:

	def __init__(self):
		pg.init()
		self.screen = pg.display.set_mode(GAME_SCREEN_SIZE)
		self.clock = pg.time.Clock()
		self.offset_x = self.offset_y = 0
		self.load = Load()

	def run(self):
		while True:
			for event in pg.event.get():
				if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
					pg.quit()
					exit()


if __name__ == "__main__":
	a = Game()
		