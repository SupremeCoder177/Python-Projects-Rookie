# PLatformer trial 4

from map import *

class Game:

	def __init__(self):
		pg.init()
		self.screen = pg.display.set_mode(SCREEN_SIZE)
		pg.display.set_caption("Platforer Trial 4")
		self.clock = pg.time.Clock()
		self.map = Map(self)
		self.player = Player(self, self.map.get_player_pos(), (TILE_SIZE // 2, TILE_SIZE), 'red')
		self.movement = [False, False]
		self.run()

	def run(self):
		while True:

			self.screen.fill('black')

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
						self.player.velocity[1] = - 15
				if event.type == pg.KEYUP:
					if event.key == pg.K_LEFT:
						self.movement[0] = False
					if event.key == pg.K_RIGHT:
						self.movement[1] = False

			self.map.draw_grid(self.screen)
			self.map.render_tiles(self.screen)
			self.player.update(self.map.get_neighbour_tiles(self.player.get_pos()), movement=self.movement)
			self.player.render(self.screen)

			pg.display.update()
			self.clock.tick(FPS)


if __name__ == '__main__':
	Game()