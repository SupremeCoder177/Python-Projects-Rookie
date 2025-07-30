# Making Pac-Man in pygame

import pygame as pg
from player import Player
from graphicsLoader import GraphicsLoader
from levelLoader import LevelLoader
from coinManager import Coins
from camera import Camera
from sys import exit
from settings import *
from time import sleep

class Game:

	def __init__(self):
		pg.init()
		pg.display.set_caption("PacMan")
		self.screen = pg.display.set_mode(GAME_SCREEN_SIZE)
		self.level_loader = LevelLoader(self)

		# seeing if the game can run a.k.a checking if there are levels to play
		if not self.level_loader.load_data():
			print("There are no levels in the levels folder, please check if you have accidently deleted it.")
			print("You can make your own levels by running levelMaker.py")
			sleep(5)
			pg.quit()
			exit()

		self.graphics = GraphicsLoader()
		self.clock = pg.time.Clock()
		self.offset_x = self.offset_y = 0
		self.player = Player(self)
		self.camera = Camera(self)
		self.coin_manager = Coins(self)
		self.delta_time = 0

	def draw(self):
		# clearing the screen
		self.screen.fill("#000000") # pure black
		# drawing the walls
		self.level_loader.draw_walls()
		# drawing the coins
		self.coin_manager.draw_coins()
		# drawing the player
		self.player.draw()

	def update(self):
		# changing offset
		# self.camera.change_offset_centered()

		# updating the coins
		self.coin_manager.update()

		# updating the player
		self.player.update()

		# updating the screen
		pg.display.flip()
		self.delta_time = self.clock.tick(FPS) / 100 # to convert to milliseconds

	def run(self):	
		while True:
			for event in pg.event.get():
				if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
					pg.quit()
					exit()
			self.update()
			self.draw()


if __name__ == "__main__":
	a = Game()
	a.run()
		