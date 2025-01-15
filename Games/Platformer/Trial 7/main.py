# Platformer Trial 7

import pygame as pg
from settings import *
from sys import exit
from map import *
from player import *
import os

class Game:

	def __init__(self):
		pg.init()
		self.screen = pg.display.set_mode(GAME_SIZE)
		pg.display.set_caption("Platformer Trial 7")
		self.clock = pg.time.Clock()
		self.map = load_map('Maps//1.json') if os.name != 'posix' else load_map('Maps\\1.json')
		self.mapper = Map(self.map, self)
		self.offset = [0, 0]
		self.player = Player(self, (2, 4), 'red', self.mapper, 40, TILE_SIZE * 2)
		self.movement = [False, False]
		self.run()

	def run(self):
		while True:

			self.screen.fill('black')

			self.offset[0] = self.player.pos[0] - (self.screen.get_size()[0] // 2)
			self.offset[1] = self.player.pos[1] - (self.screen.get_size()[1] // 2)


			for event in pg.event.get():
				if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
					pg.quit()
					exit()
				if event.type == pg.KEYDOWN:
					if event.key == pg.K_LEFT:
						self.movement[0] = True
					if event.key == pg.K_RIGHT:
						self.movement[1] = True
				if event.type == pg.KEYUP:
					if event.key == pg.K_LEFT:
						self.movement[0] = False
					if event.key == pg.K_RIGHT:
						self.movement[1] = False

			self.mapper.draw_map(self.offset)
			self.player.update(self.movement, self.offset)

			pg.display.flip()
			self.clock.tick(FPS)


if __name__ == '__main__':
	Game()