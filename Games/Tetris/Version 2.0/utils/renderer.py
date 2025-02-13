# bricks renderer for tetris 

import pygame as pg
from .brickFactory import BrickFactory
from .brick import Brick, FallenBrick
from random import randint, choice


'''This class handles all the brick rendering, and also stores all the
	brick objects
'''
class Renderer:

	def __init__(self, screen : pg.display.set_mode, images : dict, data : dict) -> None:
		self.screen = screen
		self.images = images
		self.falling_brick = None
		self.bricks_on_floor = []
		self.factory = BrickFactory()
		self.data = data
		self.fall_fast = False

	'''Adds and renders a new falling brick to the screen'''
	def add_brick(self):
		# grid coors
		x = (self.data["game_size"][0] // self.data["tile_size"]) // 2
		y = -1
		self.falling_brick = Brick(self.factory.get_brick(randint(0, self.factory.type_size() - 1)), choice(list(self.images.keys())), [x, y], self.data["tile_size"])
		self.render()

	'''This function handles all the drawing of all the bricks'''
	def render(self):
		if not self.falling_brick: self.add_brick()
		# rendering the falling brick
		for coor in self.falling_brick.get_bricks():
			self.screen.blit(self.images[self.falling_brick.img], coor)

		# rendering the bricks on the floor
		for brick in self.bricks_on_floor:
			self.screen.blit(brick.img, (brick.x, brick.y))

	'''Function to apply downward movement of the falling brick'''
	def apply_gravity(self):
		temp = self.falling_brick.coor
		temp[1] += self.data["brick_fall_speed"] if not self.fall_fast else self.data["brick_increased_fall_speed"]
		self.falling_brick.coor = temp

	'''Replaces all the sub-bricks from the falling brick and append
	   them to the bricks on the floor, they are no longer falling
	'''
	def land(self):
		for coor in self.falling_brick.get_bricks():
			self.bricks_on_floor.append(FallenBrick(coor[0], coor[1], self.images[self.falling_brick.img]))
		self.falling_brick = None
		self.fall_fast = False

	'''Updates the bricks based on collisions'''
	def update(self):
		if not self.falling_brick: self.add_brick()
		if self.falling_brick.falling: self.apply_gravity()
		else: self.land()

	'''Returns the falling brick'''
	def get_falling_brick(self) -> None:
		return self.falling_brick

	'''Returns the fallen bricks'''
	def get_landed_bricks(self) -> None:
		return self.bricks_on_floor

	'''Set fall fast to true'''
	def set_fall_fast(self) -> None:
		self.fall_fast = True
