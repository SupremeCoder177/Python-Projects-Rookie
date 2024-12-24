# map

from player import *
import itertools as itr

for per in itr.permutations([-1, 0, 1], 2):
	print(per)

class Map:

	def __init__(self, game):
		self.game = game
		self.tiles = []
		self.load_tiles()

	def load_tiles(self):
		for row_index, row in enumerate(TILE_MAP):
			for col_index, col in enumerate(row):
				if col == 1:
					self.tiles.append(pg.Rect(col_index * TILE_SIZE, row_index * TILE_SIZE, TILE_SIZE, TILE_SIZE))
				if col == 2:
					self.player_pos = [col_index, row_index]

	def render_tiles(self, surf):
		for tile in self.tiles:
			pg.draw.rect(surf, 'gray', tile)

	def draw_grid(self, surf):
		for x in range(surf.get_width() // TILE_SIZE):
			for y in range(surf.get_height() // TILE_SIZE):
				pg.draw.rect(surf, 'blue', (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

	def get_neighbour_tiles(self, pos):
		neight_tiles_pos = [
		[pos[0], pos[1]],
		[pos[0] - 1, pos[1]],
		[pos[0] + 1, pos[1]],
		[pos[0] - 1, pos[1] - 1],
		[pos[0], pos[1] - 1],
		[pos[0] + 1, pos[1] - 1],
		[pos[0] - 1, pos[1] + 1],
		[pos[0], pos[1] + 1],
		[pos[0] + 1, pos[1] + 1],
		]
		tiles = []

		for offset in neight_tiles_pos:
			if pg.Rect(offset[0] * TILE_SIZE, offset[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE) in self.tiles:
				tiles.append(pg.Rect(offset[0] * TILE_SIZE, offset[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))
		return tiles


	def get_player_pos(self):
		return self.player_pos