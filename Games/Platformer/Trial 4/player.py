# Player

from settings import *

class Player:

	def __init__(self, game, pos, size, color):
		self.game = game
		self.color = color
		self.player_rect = pg.Rect(pos[0] * TILE_SIZE, pos[1] * TILE_SIZE, size[0], size[1])
		self.velocity = [5, 0]
		self.moving = {
		"up" : False,
		"down" : False,
		"left" : False,
		"right" : False
		}

	def update(self, tilemap, movement=(0, 0)):
		self.moving = {
		"up" : False,
		"down" : False,
		"left" : False,
		"right" : False
		}

		rect_move = [(movement[1] - movement[0]) * self.velocity[0], self.velocity[1]]

		self.player_rect.x += rect_move[0]
		for tile in tilemap:
			if self.player_rect.colliderect(tile):
				if movement[0]:
					self.player_rect.left = tile.right
					self.moving['left'] = True
				if movement[1]:
					self.player_rect.right = tile.left
					self.moving['right'] = True

		self.player_rect.y += rect_move[1]
		for tile in tilemap:
			if self.player_rect.colliderect(tile):
				if self.velocity[1] > 0:
					self.player_rect.bottom = tile.top
					self.moving['down'] = True
					
				if self.velocity[1] < 0:
					self.player_rect.top = tile.bottom
					self.moving['up'] = True
				self.velocity[1] = 0

		self.velocity[1] = min(10, self.velocity[1] + 1)

	def render(self, surf):
		pg.draw.rect(surf, self.color, self.player_rect)

	def get_pos(self):
		return [int(self.player_rect.x // TILE_SIZE), int(self.player_rect.y // TILE_SIZE)]
