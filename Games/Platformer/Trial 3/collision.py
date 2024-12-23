# Collision 

from map import *

class Collision:

	def __init__(self, screen, player, map_):
		self.player = player
		self.player_pos = self.player.get_pos()
		self.screen = screen
		self.map = map_
		self.colide_tiles = {}
		self.check_primitive_collision()

	def get_neighbour_tiles(self):
		self.top_tiles = [[self.player_pos[0] - 1, self.player_pos[1] - 1],
		[self.player_pos[0], self.player_pos[1] - 1],
		[self.player_pos[0] + 1, self.player_pos[1] - 1]]

		self.bottom_tiles = [[self.player_pos[0] - 1, self.player_pos[1] + 1],
		[self.player_pos[0], self.player_pos[1] + 1],
		[self.player_pos[0] + 1, self.player_pos[1] + 1]]

		self.left_tiles = [
		[self.player_pos[0] - 1, self.player_pos[1]],
		[self.player_pos[0] - 1, self.player_pos[1] - 1],
		[self.player_pos[0] - 1, self.player_pos[1]  +1]
		]

		self.right_tiles = [
		[self.player_pos[0] + 1, self.player_pos[1]],
		[self.player_pos[0] + 1, self.player_pos[1] - 1],
		[self.player_pos[0] + 1, self.player_pos[1]  +1]
		]

		return [
		[self.player_pos[0] - 1, self.player_pos[1] - 1],
		[self.player_pos[0], self.player_pos[1] - 1],
		[self.player_pos[0] + 1, self.player_pos[1] - 1],
		[self.player_pos[0] - 1, self.player_pos[1]],
		[self.player_pos[0] + 1, self.player_pos[1]],
		[self.player_pos[0] - 1, self.player_pos[1] + 1],
		[self.player_pos[0], self.player_pos[1] + 1],
		[self.player_pos[0] + 1, self.player_pos[1] + 1],
		]

	def filter_tiles(self, tiles):
		tiles = self.convert_rect(tiles)
		tiles = [tile for tile in tiles if tile in self.map.tiles]
		return tiles

	def convert_rect(self, tiles):
		return [pg.Rect(tile[0] * COL_SIZE + self.map.offset_x, tile[1] * COL_SIZE + self.map.offset_y, COL_SIZE, COL_SIZE) for tile in tiles]

	def check_primitive_collision(self):
		vertical_tiles = []
		horizontal_tiles = []
		for tile in self.filter_tiles(self.get_neighbour_tiles()):
			if self.player.player_rect.colliderect(tile):
				if tile.y <= self.player.player_rect.y <= tile.y + COL_SIZE:
					horizontal_tiles.append(tile)
				if tile.x <= self.player.player_rect.x <= tile.x + COL_SIZE:
					vertical_tiles.append(tile)
				pg.draw.rect(self.screen, 'green', tile)
		self.get_horiontal_collide_tiles(horizontal_tiles)
		self.get_vertical_collide_tiles(vertical_tiles)

	def get_vertical_collide_tiles(self, tiles):
		for tile in sorted(tiles, key=lambda t: t.y):
			if tile in self.filter_tiles(self.top_tiles):
				self.colide_tiles['vertical_up'] = tile
				continue
			if tile in self.filter_tiles(self.bottom_tiles):
				self.colide_tiles['vertical_down'] = tile
				continue

	def get_horiontal_collide_tiles(self, tiles):
		for tile in sorted(tiles, key=lambda t: t.x):
			if tile in self.filter_tiles(self.left_tiles):
				self.colide_tiles['left'] = tile
			if tile in self.filter_tiles(self.right_tiles):
				self.colide_tiles['right'] = tile

	def get_collide_tiles(self):
		return self.colide_tiles