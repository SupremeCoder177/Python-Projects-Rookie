# Making Space Invaders

import pygame as pg
from sys import exit
import os
from json import load
from entities import Player

class Game:

	def __init__(self, data : dict):
		pg.init()
		self.data = data
		self.screen = pg.display.set_mode(data["window_size"])
		pg.display.set_caption(data["game_name"])
		self.clock = pg.time.Clock()
		self.player = Player(self.screen, pg.image.load("Images/main_ship.png").convert_alpha(), 3, 0, [100, 200])
		self.move = False
		self.rotate = False
		self.amount = 1

	# this method contains the game loop
	def run(self) -> None:
		while True:
			for event in pg.event.get():
				if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
					pg.quit()
					exit()
				if event.type == pg.KEYDOWN:
					if event.key == pg.K_w:
						self.move = True
					if event.key == pg.K_LEFT:
						self.rotate = True
						self.amount = 1
					if event.key == pg.K_RIGHT:
						self.rotate = True
						self.amount = -1
				if event.type == pg.KEYUP:
					if event.key == pg.K_w:
						self.move = False
					if event.key == pg.K_LEFT:
						self.rotate = False
					if event.key == pg.K_RIGHT:
						self.rotate = False

			self.screen.fill((0, 0, 0))

			self.player.render()

			if self.move:
				self.player.move()

			if self.rotate:
				self.player.rotate(self.amount)

			self.player.show_direction("white", 1000)

			pg.display.flip()
			self.clock.tick(120)


if __name__ == '__main__':
	if "settings.json" not in os.listdir(): 
		raise FileNotFoundError("The settings were not found in the game directory, please ensure\na file named settings.json is in the game folder")
	else:
		with open("settings.json", "r") as file:
			DATA = load(file)
		game = Game(DATA)
		game.run()