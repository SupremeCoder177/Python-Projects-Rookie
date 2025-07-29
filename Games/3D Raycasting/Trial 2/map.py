# Map class

import pygame as pg
from settings import WORLD_MAP, TILE_SIZE

class Map:

	def __init__(self, game):
		self.display = game.screen
		self.world_map = []
		self.calc_tiles()

	def calc_tiles(self):
		for row_index, row in enumerate(WORLD_MAP):
			for col_index, col in enumerate(row):
				if col:
					self.world_map.append((col_index, row_index))

	def draw_map(self):
		for tile in self.world_map:
			pg.draw.rect(self.display, 'grey', (tile[0] * TILE_SIZE, tile[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

