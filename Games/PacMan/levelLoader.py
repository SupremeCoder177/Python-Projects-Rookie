# Level Loader for PacMan

import pygame as pg
from settings import *
from json import load
import os

# change this to load levels from another folder
# the reason I didn't put this variable in the settings file
# is because I think it is much more sensible to put anything
# related to loading levels inside the levelLoader file
LEVEL_LOCATION = "levels/"

# this class will calculate pixel positions of walls
# and draw them, and will be the class which handles wall collisions
class LevelLoader:

	def __init__(self, game):
		self.curr_level = CURRENT_LEVEL
		self.game = game
		self.display = game.screen
		self.levels = LEVELS
		self.data = {}
		self.world_map = []

	# loops over all the levels until it finds one which exists, then loads the data from that level
	# although it is very improbable that the user might delete some level files while playing
	# it can happen, this makes sure the game doesn't crash if some level files are deleted while game is playing
	def load_data(self):
		while self.curr_level <= MAX_LEVEL:
			if os.path.exists(f'{LEVEL_LOCATION}{self.levels[self.curr_level]}'):
				with open(f'{LEVEL_LOCATION}{self.levels[self.curr_level]}', 'r') as f:
					self.data = load(f)
					self.world_map.clear()
					self.update_wall_data()
					self.curr_level += 1
					return True
			else:
				self.curr_level += 1
		return False

	def is_blocked(self, point):
		return (int(point[0]), int(point[1])) in self.world_map

	def update_wall_data(self):
		for str_pos in self.data["world_map"]:
			x, y = str_pos.split(',')
			tile_pos = int(x), int(y)
			self.world_map.append(tile_pos)

	def draw_walls(self):
		for str_pos, wall_type in self.data["world_map"].items():
			x, y = str_pos.split(",")
			world_pos = int(x) * TILE_SIZE + self.game.offset_x, int(y) * TILE_SIZE + self.game.offset_y
			wall_surf = self.game.graphics.walls[wall_type]
			self.display.blit(wall_surf, world_pos)

		