# player

from settings import *
import pygame as pg

class Player:

	def __init__(self, game, pos, color, mapper, width, height):
		self.game = game
		self.pos = [pos[0] * TILE_SIZE, pos[1] * TILE_SIZE]
		self.color = color
		self.velocity = [5, 0]
		self.mapper = mapper
		self.width = width
		self.height = height

	def update(self, movement, offset):
		frame_movement = [int(movement[1] - movement[0]) * self.velocity[0], self.velocity[1]]

		self.pos[0] += frame_movement[0]
		for tile in self.get_neighbour_tiles():
			temp = pg.Rect(self.pos[0], self.pos[1], self.width, self.height)
			if temp.colliderect(tile):
				if movement[0]:
					self.pos[0] = tile.x + TILE_SIZE
				if movement[1]:
					self.pos[0] = tile.x - TILE_SIZE

		self.pos[1] += frame_movement[1]
		for tile in self.get_neighbour_tiles():
			temp = pg.Rect(self.pos[0], self.pos[1], self.width, self.height)
			if temp.colliderect(tile):
				if self.velocity[1] > 0:
					self.pos[1] = tile.y - self.height
				if self.velocity[1] < 0:
					self.pos[1] = tile.y + TILE_SIZE
				self.velocity[1] = 0

		print(self.pos[1])

		self.velocity[1] = min(10, self.velocity[1] + 0.1)

		self.draw_player(offset)

	def draw_player(self, offset):
		pg.draw.rect(self.game.screen, self.color, (self.pos[0] - offset[0], self.pos[1] - offset[1], self.width, self.height))

	def get_neighbour_tiles(self):
		NEIGHBOUT_OFFSET = [(-1, -1), (0, -1), (1, -1),
		(-1, 0), (1, 0),
		(-1, 1), (0, 1), (1, 1)]

		temp = []
		for offset in NEIGHBOUT_OFFSET:
			x = int(self.pos[0] // TILE_SIZE) + offset[0]
			y = int(self.pos[1] // TILE_SIZE) + offset[1]
			if (x, y) in self.mapper.map: temp.append(pg.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

		return temp
		

