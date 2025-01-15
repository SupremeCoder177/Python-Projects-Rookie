# Map Class

from settings import *
import pygame as pg


class Map:

	def __init__(self, map_, game):
		self.game = game
		self.map = map_
		self.convert()

	def convert(self):
		temp_ = {}
		for pos in self.map:
			temp = tuple(map(int, pos.split(';')))
			temp_[temp] = self.map[pos]
		self.map.clear()
		self.map = temp_.copy()

	def draw_map(self, offset):
		for rect in self.map:
			if self.map[rect]['fill']:
				pg.draw.rect(self.game.screen, self.map[rect]['color'], ((rect[0] * TILE_SIZE) - offset[0], (rect[1] * TILE_SIZE) - offset[1], TILE_SIZE, TILE_SIZE))
			else:
				pg.draw.rect(self.game.screen, self.map[rect]['color'], ((rect[0] * TILE_SIZE) - offset[0], (rect[1] * TILE_SIZE) - offset[1], TILE_SIZE, TILE_SIZE), 1)