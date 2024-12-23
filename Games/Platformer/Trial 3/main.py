# Platformer trial 3

from camera import *

class Game:

	def __init__(self):
		pg.init()
		self.screen = pg.display.set_mode(SCREEN_SIZE)
		pg.display.set_caption("Platformer Trial 3")
		self.clock = pg.time.Clock()
		self.map = Map(self.screen)
		self.player = Player(self.screen, self.map, 'red', COL_SIZE / 2, COL_SIZE)
		self.camera = Camera(self.player, self.map)
		self.run()

	def run(self):
		while True:
			for event in pg.event.get():
				if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
					pg.quit()
					exit()

			self.screen.fill('black')

			self.camera.update()
			self.map.update('blue', 'gray')
			self.player.update(True)

			pg.display.flip()
			self.clock.tick(FPS)



if __name__ == '__main__':
	Game()