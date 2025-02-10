# Making a better version of tetirs

import pygame as pg
import logging
from json import load
from sys import exit
from random import randint
from utils.DictImages import dictionarize_imgs
from utils.renderer import Renderer
import os


'''Class to contain all game logic and elements'''
class Game:

	def __init__(self):
		self.logger = logging.getLogger(__name__)
		self.load_settings()
		pg.init()
		self.screen = pg.display.set_mode(self.data["window_size"])
		self.clock = pg.time.Clock()
		self.renderer = Renderer(self.screen, dictionarize_imgs(os.path.abspath('Images'), ".png"), self.data["tile_size"], self.data["brick_fall_speed"])
		pg.display.set_caption(self.data["game_name"])
		self.run()

	def draw_grid(self):
		# function to draw a rainbow grid according to given game size
		tile_size = self.data["tile_size"]
		width = self.data["game_size"][0]
		height = self.data["game_size"][1]
		x_offset = self.data["game_grid_start_x"]
		y_offset = self.data["game_grid_start_y"]
		color = self.data["grid_color"]
		for x in range(width // tile_size):
			for y in range(height // tile_size):
				pg.draw.rect(self.screen, tuple(color), ((x * tile_size) + x_offset, (y * tile_size) + y_offset, tile_size, tile_size), 1, 3)
			color = [min(255, val + randint(10, 20)) for val in color]


	def run(self):
		'''Function to contain the game loop, no threading is used for this game'''
		while True:
			# event loop
			for event in pg.event.get():
				if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
					pg.quit()
					exit()

			# clearing screen
			self.screen.fill((0, 0, 0)) # black

			# drawing a grid
			self.draw_grid()

			# rendering bricks
			self.renderer.render()

			# updating bricks
			self.renderer.update()

			#updating the screen
			pg.display.flip()
			self.clock.tick(self.data["fps"])

	def load_settings(self):
		'''Loading the settings from json file, (warning) if settings is not in current working directory
		   then an error will be thrown
		'''
		try:
			with open("settings.json", 'r') as file:
				self.data = load(file)
		except Exception as e:
			self.logger.debug(f'Error {e} has occured')



if __name__ == "__main__":
	Game()

