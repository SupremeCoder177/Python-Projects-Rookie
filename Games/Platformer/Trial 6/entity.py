# physics

from settings import *

class Entity:

	def __init__(self, game, size, pos, color):
		self.game = game
		self.rect = pg.Rect(pos[0] * TILE_SIZE, pos[1] * TILE_SIZE, size[0], size[1])
		self.color = color
		self.velocity = [0, 0]
		self.fall = False
		self.fall_speed_max = 0
		self.acc = 0

	def update(self, movement, tiles):
		frame_movement = [(movement[1] - movement[0]) * self.velocity[0], self.velocity[1]]

		self.rect.x += frame_movement[0]
		for tile in tiles:
			if self.rect.colliderect(tile):
				if movement[0]:
					self.rect.left = tile.right
				if movement[1]:
					self.rect.right = tile.left
		self.rect.y += frame_movement[1]
		if self.fall:
			for tile in tiles:
				if self.rect.colliderect(tile):
					if self.velocity[1] > 0:
						self.rect.bottom = tile.top
						self.velocity[1] = 0
					if self.velocity[1] < 0:
						self.rect.top = tile.bottom
						self.velocity[1] = 0

		if self.fall: self.velocity[1] = min(self.fall_speed_max, self.velocity[1] + self.acc)

	def render(self, surf, offset):
		temp = self.rect.copy()
		temp.x -= offset[0]
		temp.y -= offset[1]
		pg.draw.rect(surf, self.color, temp)

	def get_pos(self):
		return [int(self.rect.x // TILE_SIZE), int(self.rect.y // TILE_SIZE)]


class Player(Entity):

	def __init__(self, game, size, pos, color):
		super().__init__(game, size, pos, color)
		self.velocity = [5, 0]
		self.fall = True
		self.acc = 1
		self.fall_speed_max = 10
