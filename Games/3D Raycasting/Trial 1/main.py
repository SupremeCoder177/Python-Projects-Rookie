# main game file

import pygame as pg
from sys import exit
from settings import *
from map import Map
from player import Player
from raycasting import RayCast

class Game:

	def __init__(self):
		pg.init()
		pg.display.set_caption("Raycasting Trial 1")
		self.screen = pg.display.set_mode(SCREEN_SIZE)
		self.clock = pg.time.Clock()
		self.map = Map(self)
		self.player = Player(self)
		self.ray_cast = RayCast(self)
		self.delta_time = 1

	# updates every entity on screen
	def update(self):
		self.player.update()
		self.ray_cast.update()

	# draws every entity on screen
	def draw(self):
		#self.map.draw()
		self.ray_cast.draw()
		#self.player.draw()

	def run(self):
		while True:
			for event in pg.event.get():
				if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE: 
					pg.quit()
					exit()

			self.screen.fill("black")

			self.update()
			self.draw()

			pg.display.flip()
			self.delta_time = self.clock.tick(FPS) 


if __name__ == "__main__":
	Game().run()