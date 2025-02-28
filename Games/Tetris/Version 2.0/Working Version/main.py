# Working version of tetris 2.0

import pygame as pg
from json import load
from os import listdir, getcwd
from sys import exit
from random import randint
from brick import *
from handler import Handler

# exiting if json file not in cwd
if not "settings.json" in listdir(getcwd()):
	exit()

# loading settings from json file in project folder
with open("settings.json", 'r') as f:
	DATA = load(f)


class Game:

	def __init__(self, data):
		pg.init()
		self.data = data
		self.screen = pg.display.set_mode(self.data["screen_size"])
		pg.display.set_caption(self.data["game_name"])
		self.clock = pg.time.Clock()
		self.manager = BricksManager(self.screen, self.data)
		self.handler = Handler(self.manager)
		self.manager.add_brick()
		self.timer = 1 / self.data["brick_fall_speed"]
		self.input_timer = 0.3
		self.last_update_time = 0
		self.last_handle_time = 0

	# method to draw a grid on the screen
	def draw_grid(self):
		x_offset = self.data["grid_x_offset"]
		y_offset = self.data["grid_y_offset"]
		grid_size = self.data["grid_size"]
		tile_size = self.data["tile_size"]
		colour = self.data["grid_color"]

		for i in range(grid_size[0] // tile_size):
			for j in range(grid_size[1] // tile_size):
				pg.draw.rect(self.screen, colour, (i * tile_size, j * tile_size, tile_size, tile_size), 1)

	def check_line(self):
		rows = self.data["grid_size"][0] // self.data["tile_size"] 
		columns = self.data["grid_size"][0] // self.data["tile_size"]
		for i in range(rows):
			full_line = True
			for j in range(columns):
				if not (j * self.data["tile_size"], i * self.data["tile_size"]) in self.manager.get_occupied():
					full_line = False
					break
			if full_line:
				self.manager.move_down_occupied(i)

	# method to run the main game window
	def run(self):
		while True:
			current_time = pg.time.get_ticks() / 1000

			for event in pg.event.get():
				if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
					pg.quit()
					exit()
				else:
					self.handler.change_input_state(event)

			# clearing the screen
			self.screen.fill((0, 0, 0)) # black

			# logic updates
			if current_time - self.last_update_time >= self.timer:
				self.manager.update()
				self.last_update_time = current_time
			if current_time - self.last_handle_time >= self.input_timer:
				self.handler.handle()
				self.last_handle_time = current_time

			# rendeting updates
			self.draw_grid()
			self.manager.render()

			# checking line
			self.check_line()

			# updating the screen
			pg.display.flip()
			self.clock.tick(self.data["fps"])


if __name__ == '__main__':
	game = Game(DATA)
	game.run()