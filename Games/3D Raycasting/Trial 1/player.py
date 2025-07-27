# player

import pygame as pg
import math
from settings import *

class Player:

	def __init__(self, game):
		self.display = game.screen
		self.map = game.map
		self.game = game
		self.pos = [PLAYER_POS[0], PLAYER_POS[1]]
		self.angle = PLAYER_ANGLE

	def draw(self):
		#direction player is looking in
		# x = (self.pos[0] * TILE_SIZE) + math.cos(self.angle) * 1000
		# y = (self.pos[1] * TILE_SIZE) + math.sin(self.angle) * 1000
		# pg.draw.line(self.display, 'yellow', (self.pos[0] * TILE_SIZE, self.pos[1] * TILE_SIZE), (x, y))

		# player
		pg.draw.circle(self.display, 'red', (self.pos[0] * TILE_SIZE, self.pos[1] * TILE_SIZE), 10)

	def take_input(self):
		keys = pg.key.get_pressed()

		if keys[pg.K_LEFT]:
			self.angle -= PLAYER_ROT_SPEED
		if keys[pg.K_RIGHT]:
			self.angle += PLAYER_ROT_SPEED

		dx = math.cos(self.angle) * PLAYER_MOVE_SPEED
		dy = math.sin(self.angle) * PLAYER_MOVE_SPEED
		if keys[pg.K_w]:
			self.check_collision(dx, dy)

	def check_collision(self, dx, dy):
		if not self.map.is_occupied(self.world_pos(self.pos[0] + dx, self.pos[1])):
			self.pos[0] += dx
		if not self.map.is_occupied(self.world_pos(self.pos[0], self.pos[1] + dy)):
			self.pos[1] += dy
		
	def update(self):
		self.angle %= math.tau
		self.take_input()

	def world_pos(self, x, y):
		return (int(x), int(y))

	def map_pos(self):
		return (self.pos[0] * TILE_SIZE, self.pos[1] * TILE_SIZE)

	def tile_pos(self):
		return (int(self.pos[0]), int(self.pos[1]))
