# Main File

import pygame as pg
from sys import exit
from settings import *
from map import Map
from player import Player
from raycasting import RayCasting

class Game:

	def __init__(self):
		pg.init()
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		self.clock = pg.time.Clock()
		self.delta_time = 0
		self.map = Map(self)
		self.player = Player(self)
		self.ray_cast = RayCasting(self)

	def update(self):
		pg.display.flip()
		self.player.update()
		pg.display.set_caption(f'{self.clock.get_fps()}')
		self.delta_time = self.clock.tick(FPS)

	def draw(self):
		self.screen.fill("black")
		self.map.draw_map()
		self.player.draw()
		#self.ray_cast.cast_rays()
		self.ray_cast.march_rays()

	def run(self):
		while True:
			for event in pg.event.get():
				if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
					pg.quit()
					exit()
			self.update()
			self.draw()


if __name__ == "__main__":
	Game().run()