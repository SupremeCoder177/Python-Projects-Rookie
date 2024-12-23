# Map

from settings import *


class Map:

	def __init__(self, screen, tile_map=TILE_MAP):
		self.screen = screen
		self.tiles = []
		self.plyer_pos = []
		self.offset_x = 0
		self.offset_y = 0
		self.tile_map = tile_map
		self.load_tiles()

	def load_tiles(self):
		for row_index, row in enumerate(self.tile_map):
			for col_index, col in enumerate(row):
				if col and col != 2:
					self.tiles.append(pg.Rect(col_index * COL_SIZE, row_index * COL_SIZE, COL_SIZE, COL_SIZE))
				elif col and col == 2:
					self.plyer_pos = [col_index, row_index]

	def update(self, grid_clr, tile_clr):
		self.draw_grid(grid_clr)
		self.draw_tiles(tile_clr)

	def draw_tiles(self, color):
		for tile in self.tiles:
			pg.draw.rect(self.screen, color, tile)

	def draw_grid(self, color):
		for row_index, row in enumerate(self.tile_map):
			for col_index, col in enumerate(row):
				pg.draw.rect(self.screen, color, (col_index * COL_SIZE, row_index * COL_SIZE, COL_SIZE, COL_SIZE), 1)

	def get_player_pos(self):
		return self.plyer_pos

	def shift(self, delta_x, delta_y):
		for tile in self.tiles:
			tile.x += delta_x
			tile.y += delta_y

		self.offset_x = self.tiles[0].x % COL_SIZE
		self.offset_y = self.tiles[0].y % COL_SIZE
