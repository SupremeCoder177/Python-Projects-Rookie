# player

from settings import *


class Player:

	def __init__(self, game):
		self.get_player_start_pos()
		self.game = game
		self.velocity = [5, 0]

	def update(self, movement, map_, offset, tile_size=TILE_SIZE):
		self.player_rect.width = tile_size / 2
		self.player_rect.height = tile_size

		frame_movement = [(movement[1] - movement[0]) * self.velocity[0], self.velocity[1]]

		self.player_rect.x += frame_movement[0]
		
		for tile in map_.get_neighbour_tiles(self.player_pos(offset)):
			if self.player_rect.colliderect(tile):
				if movement[0]:
					self.player_rect.left = tile.right
				if movement[1]:
					self.player_rect.right = tile.left

		self.player_rect.y += frame_movement[1]
		for tile in map_.get_neighbour_tiles(self.player_pos(offset)):
			if self.player_rect.colliderect(tile):
				if self.velocity[1] > 0:
					self.player_rect.bottom = tile.top
					self.velocity[1] = 0
				if self.velocity[1] < 0:
					self.player_rect.top = tile.bottom
					self.velocity[1] = 0

		self.velocity[1] = min(10, self.velocity[1] + 1)

	def render(self, surf, offset):
		temp = self.player_rect.copy()
		temp.x -= offset[0]
		temp.y -= offset[1]
		pg.draw.rect(surf, 'red', temp)

	def get_player_start_pos(self):
		for row in TILE_MAP:
			if 2 in row:
				self.player_rect = pg.Rect(row.index(2) * TILE_SIZE, TILE_MAP.index(row) * TILE_SIZE, TILE_SIZE / 2, TILE_SIZE)

	def player_pos(self, offset, tile_size = TILE_SIZE):
		return [int(self.player_rect.x // tile_size), int(self.player_rect.y // tile_size)]