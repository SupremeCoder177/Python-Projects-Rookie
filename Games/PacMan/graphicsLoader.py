# Graphics Loader for PacMan

import pygame as pg
from settings import *

class Load:

	def __init__(self):
		self.sprites_total = 0
		self.sprites = dict()
		self.load_wall_images()

	# loads the png frames of each wall type from the graphics folder in current working directory
	def load_wall_images(self):
		image = pg.image.load("graphics/walls.png").convert_alpha()
		for i in range(image.get_width() // WALL_WIDTH):
			for j in range(image.get_height() // WALL_HEGIHT):
				temp = pg.Surface((WALL_WIDTH, WALL_HEGIHT))
				temp.blit(image, (0, 0), (i * WALL_WIDTH, j * WALL_HEGIHT, WALL_WIDTH, WALL_HEGIHT))
				self.sprites[self.sprites_total] = {"wall" + str(i) : temp}
				self.sprites_total += 1

	def load_player_images(self):
		pass

	def load_enemy_images(self):
		pass

