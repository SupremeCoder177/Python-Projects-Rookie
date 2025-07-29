# Player

import pygame as pg
from math import *
from settings import *

class Player:

	def __init__(self, game):
		self.display = game.screen
		self.pos = PLAYER_START_POSITION
		self.angle = PLAYER_ANGLE
		self.game = game
		self.map = game.map

	# draws the player in 2D
	def draw(self):
		# direction the player is looking in
		pg.draw.line(self.display, 'yellow', self.map_pos(),
			self.end_point(WIDTH))

		# player itself
		pg.draw.circle(self.display, 'red', self.map_pos(), 10)

	# checks player collision with the walls
	def check_collision(self, dx, dy):
		if (int(self.pos[0] + dx), int(self.pos[1])) not in self.map.world_map:
			self.pos[0] += dx
		if (int(self.pos[0]), int(self.pos[1] + dy)) not in self.map.world_map:
			self.pos[1] += dy

	# takes in keyboard input from the user
	def take_input(self):
		keys = pg.key.get_pressed()

		SPEED = PLAYER_SPEED * self.game.delta_time
		dx = cos(self.angle) * SPEED
		dy = sin(self.angle) * SPEED

		# rotating player direction
		if keys[pg.K_LEFT]:
			self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
		if keys[pg.K_RIGHT]:
			self.angle += PLAYER_ROT_SPEED * self.game.delta_time

		# moving the player
		if keys[pg.K_w]:
			self.check_collision(dx, dy)
		if keys[pg.K_s]:
			self.check_collision(-dx, -dy)
		if keys[pg.K_a]:
			self.check_collision(dx, -dy)
		if keys[pg.K_d]:
			self.check_collision(-dx, dy)

	# checks collisions and takes in input
	def update(self):
		self.take_input()
		# to make sure player angle is always in between 0 and 2 * pi
		self.angle %= tau # tau = 2 * pi

	# return pixel coordinate of the player
	def map_pos(self):
		return self.pos[0] * TILE_SIZE, self.pos[1] * TILE_SIZE

	# return tile coordinate of the player
	def tile_pos(self):
		return int(self.pos[0]), int(self.pos[1])

	# length is in tile length not pixels
	def end_point(self, length):
		return (self.pos[0] + length * cos(self.angle)) * TILE_SIZE, (self.pos[1] + length * sin(self.angle)) * TILE_SIZE