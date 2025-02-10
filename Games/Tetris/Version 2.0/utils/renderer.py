# bricks renderer for tetris 

import pygame as pg
from .brickFactory import BrickFactory
from .brick import Brick
from random import randint, choice

class Renderer:

	def __init__(self, screen : pg.display.set_mode, images : dict, tile_size : int, fall_speed : int) -> None:
		self.screen = screen
		self.images = images
		self.bricks = []
		self.factory = BrickFactory()
		self.fall_speed = fall_speed

	def add_brick(self):
		self.bricks.append(Brick(self.factory.get_brick(randint(0, self.factory.type_size() - 1)), choice(images)))

	def render(self):
		pass

	def update(self):
		pass
