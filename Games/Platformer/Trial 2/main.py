# Making platformer in python


from player import *
from time import time


class Game:

	def __init__(self):
		pg.init()
		self.screen = pg.display.set_mode(SCREEN_SIZE)
		pg.display.set_caption('Platformer Trial 2')
		self.map = Map(self.screen, TILE_MAP)
		self.player = Player(self.screen, self.map.get_player_pos(), COL_SIZE // 2, COL_SIZE, 'red')
		self.clock = pg.time.Clock()
		self.run()

	def check_collision(self):
		player = self.player.get_pos()
		neighbour_tiles = (
			[player[0], player[1] - 1],
			[player[0], player[1] + 1],
			[player[0] - 1, player[1] - 1],
			[player[0] -1, player[1]],
			[player[0] - 1,  player[1] + 1],
			[player[0] + 1, player[1] - 1],
			[player[0] + 1, player[1]],
			[player[0] + 1, player[1] + 1])

		tiles = []
		for tile in neighbour_tiles:
			tiles.append(pg.Rect(tile[0] * COL_SIZE + self.map.offset_x, tile[1] * COL_SIZE + self.map.offset_y, COL_SIZE, COL_SIZE))

		tiles = [tile for tile in tiles if tile in self.map.tiles]

		for tile in tiles:
			if self.player.player.colliderect(tile):
				colided = True
				if tile.y <= self.player.player.y <= tile.y + COL_SIZE:
					if self.player.direction_x[0]:
						print('left')
					if self.player.direction_x[1]:
						print('right')
				if tile.x <= self.player.player.x <= tile.x + COL_SIZE:
					if self.player.direction_y[1] and self.player.player.y + COL_SIZE >= tile.y:
						self.player.player.bottom = tile.top
						self.player.stop_velocity = True
					if self.player.direction_y[0]:
						self.player.player.top = tile.bottom
						self.player.velocity = 0
				pg.draw.rect(self.screen, 'green', tile)

	def check_player_pos(self):
		player = self.player.player
		if player.left <= (2 * COL_SIZE) and self.player.direction_x[0]:
			self.map.shift(PLAYER_SPEED, 0)
			self.player.player_speed = 0
		elif player.right >= SCREEN_SIZE[0] - (2 * COL_SIZE) and self.player.direction_x[1]:
			self.map.shift(-PLAYER_SPEED, 0)
			self.player.player_speed = 0
		else:
			self.player.player_speed = PLAYER_SPEED

	def run(self):
		while True:
			for event in pg.event.get():
				if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
					pg.quit()
					exit()

			curr_time = time()
			self.screen.fill('black')

			self.check_player_pos()
			self.map.draw_grid('blue')
			self.map.draw_tiles('gray')
			self.check_collision()
			self.player.update()

			after_time = time()

			# print(self.clock.get_fps())
  
			pg.display.flip()
			self.clock.tick(FPS)


if __name__ == '__main__':
	Game()