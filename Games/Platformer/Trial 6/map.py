from settings import *


class Map:

	def __init__(self, game):
		self.game = game

	def render(self, surf, tiles, offset, tile_size=TILE_SIZE):
		for tile in tiles:
			x = str()
			y = str()
			semi = False
			for ch in tile:
				if ch == ';': 
					semi = True
					continue
				if not semi: x += ch
				if semi: y += ch

			temp = pg.Rect(int(x) * tile_size, int(y) * tile_size, tile_size, tile_size)
			temp.x -= offset[0]
			temp.y -= offset[1]
			pg.draw.rect(surf, 'gray', temp, 1)

	def get_neighbour_tiles(self, pos, tiles, tile_size=TILE_SIZE):
		NEIGHBOUR_OFFSET = [
		(-1, 1), (0, 1), (1, 1),
		(-1, 0), (0, 0), (1, 0),
		(-1, -1), (0, -1), (1, -1)
		]

		rects = []
		for offset in NEIGHBOUR_OFFSET:
			tile_key = f'{pos[0] + offset[0]};{pos[1] + offset[1]}'
			if tile_key in tiles:
				if tiles[tile_key]['physics']:
					rects.append(pg.Rect((pos[0] + offset[0]) * tile_size, (pos[1] + offset[1]) * tile_size, tile_size, tile_size))

		return rects