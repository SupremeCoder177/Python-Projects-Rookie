from map import *
from settings import *
from entity import *

class Game:

	def __init__(self):
		pg.init()
		self.screen = pg.display.set_mode(SCREEN_SIZE)
		pg.display.set_caption("Platformer Trial 6")
		self.clock = pg.time.Clock()
		self.map = Map(self)
		self.player = Player(self, (TILE_SIZE // 2, TILE_SIZE), (2, 1), 'red')
		self.tiles = TILE_MAP
		self.movement = [False, False]
		self.offset = [0, 0]
		self.run()

	def run(self):
		while True:
			self.screen.fill('black')

			self.offset[0] = self.player.rect.centerx - (self.screen.get_width() / 2)
			self.offset[1] = self.player.rect.centery - (self.screen.get_height() / 2)

			for event in pg.event.get():
				if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
					pg.quit()
					exit()
				if event.type == pg.KEYDOWN:
					if event.key == pg.K_LEFT:
						self.movement[0] = True
					if event.key == pg.K_RIGHT:
						self.movement[1] = True
					if event.key == pg.K_SPACE:
						self.player.velocity[1] = -13
				if event.type == pg.KEYUP:
					if event.key == pg.K_LEFT:
						self.movement[0] = False
					if event.key == pg.K_RIGHT:
						self.movement[1] = False

			self.map.render(self.screen, self.tiles, self.offset)

			self.player.update(self.movement, self.map.get_neighbour_tiles(self.player.get_pos(), self.tiles))
			self.player.render(self.screen, self.offset)

			pg.display.update()
			self.clock.tick(FPS)


if __name__ == '__main__':
	Game()
