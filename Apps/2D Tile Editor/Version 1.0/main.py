# the game editor I always wanted to make

import pygame as pg
from sys import exit
from json import load
from loadScreen import LoadingScreen
from appSettings import *


class App:

	def __init__(self):
		pg.init()
		self.main_screen = pg.display.set_mode(SETTINGS["app_size"])
		pg.display.set_caption("2D Tile Editor")
		self.clock = pg.time.Clock()

		# frame events handler vars
		self.frames_elapsed = 0
		self.max_frames_elapsed = 10e5

		# the different screen
		loading_screen = LoadingScreen(self, loading_screen_settings)
		self.sub_screens = [loading_screen]

		# selecting the current scrren
		self.curr_screen = 0

	def run(self):
		while True:
			mouse_pos = pg.mouse.get_pos()

			for event in pg.event.get():
				if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
					pg.quit()
					exit()

				if event.type == pg.KEYDOWN:
					# a short cut to change between screen
					if event.key == pg.K_k:
						self.curr_screen += 1
						self.curr_screen %= len(self.sub_screens)
			
			# don't change this pls
			self.frames_elapsed += 1
			self.frames_elapsed %= self.max_frames_elapsed

			# clearing the screen
			self.main_screen.fill((0, 0, 0))

			# drawing the current selected sub-screen
			self.sub_screens[self.curr_screen].draw(self.main_screen)

			pg.display.update()
			self.clock.tick(SETTINGS["fps"])


if __name__ == "__main__":
	a = App()
	a.run()