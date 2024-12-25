# Plaformer Trial 5

from map import *


class Game:

	def __init__(self):
		pg.init()
		self.screen = pg.display.set_mode(SCREEN_SIZE)
		pg.display.set_caption("Platformer Trial 5")
		self.clock = pg.time.Clock()
		self.player = Player(self)
		self.map = Map(self)
		self.movement = [False, False]
		self.offset = pg.math.Vector2(0, 0)
		self.half_w = self.screen.get_size()[0] // 2
		self.tile_size = TILE_SIZE
		self.half_h = self.screen.get_size()[1] // 2
		self.run()

	def run(self):
		while True:
			self.screen.fill('black')

			self.offset.x = self.player.player_rect.centerx - self.half_w
			self.offset.y = (self.player.player_rect.centery - self.half_h) - TILE_SIZE

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
						self.player.velocity[1] = -15	
				if event.type == pg.KEYUP:
					if event.key == pg.K_LEFT:
						self.movement[0] = False
					if event.key == pg.K_RIGHT:
						self.movement[1] = False

			self.map.render(self.screen, self.offset)
			self.player.update(self.movement, self.map, self.offset)
			self.player.render(self.screen, self.offset)

			pg.display.update()
			self.clock.tick(FPS)


if __name__ == '__main__':
	Game()