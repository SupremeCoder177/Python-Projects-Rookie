# map

from player import *

class Map:

	def __init__(self, game):
		self.game = game
		self.tiles = []
		self.load_tiles()

	def load_tiles(self, tile_size=TILE_SIZE):
		self.tiles.clear()
		for row_index, row in enumerate(TILE_MAP):
			for col_index, col in enumerate(row):
				if col == 1:
					self.tiles.append(pg.Rect(col_index * tile_size, row_index * tile_size, tile_size, tile_size))

	def get_neighbour_tiles(self, pos):
		NEIGHBOUR_OFFSETS = [
		[pos[0] - 1, pos[1] - 1],
		[pos[0], pos[1] - 1],
		[pos[0] + 1, pos[1] - 1],
		[pos[0] - 1, pos[1]],
		[pos[0], pos[1]],
		[pos[0] + 1, pos[1]],
		[pos[0] - 1, pos[1] + 1],
		[pos[0], pos[1] + 1],
		[pos[0] + 1, pos[1] + 1],
		]

		tiles = [pg.Rect(pos_[0] * TILE_SIZE, pos_[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE) for pos_ in NEIGHBOUR_OFFSETS]
		
		return [tile for tile in tiles if tile in self.tiles]

	def render(self, surf, offset):
		for tile in self.tiles:
			temp = tile.copy()
			temp.x -= offset[0]
			temp.y -= offset[1]
			pg.draw.rect(surf, 'gray', temp, 1)