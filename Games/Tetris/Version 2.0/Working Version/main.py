# Making another version of tetris 2.0 (working this time)

import pygame as pg
from sys import exit
from json import load

class Game:

	def __init__(self):
		self.load_settings()
		pg.init()
		self.screen = pg.display.set_mode(self.data["window_size"])
		pg.display.set_caption(self.data["game_name"])
		self.clock = pg.time.Clock()
		self.run()

	'''Main Game Loop (this game uses no threads)'''
	def run(self):
		while True:
			# checking for user event
			for event in pg.event.get():
				if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
					pg.quit()
					exit()

			# clearing the screen
			self.screen.fill((0, 0, 0)) # black

			# refreshing the screen
			pg.display.flip()
			self.clock.tick(self.data["fps"])

	def load_settings(self):
		'''Loading the settings from json file, (warning) if settings is not in current working directory
		   then an error will be thrown
		'''
		try:
			with open("settings.json", 'r') as file:
				self.data = load(file)
		except Exception as e:
			exit()


if __name__ == '__main__':
	Game()
