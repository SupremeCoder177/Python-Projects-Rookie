# the game editor I always wanted to make

import pygame as pg
from sys import exit
from widgets.frame import Frame, RightClickFrame
from widgets.buttons import Button
from json import load
from os import getcwd


class App:

	def __init__(self):
		self.load_data()

		if not self.settings:
			print("Failed to load settings, check to see if 'settings.json' in current working directory")
			print(f"Current directory : {getcwd()}")
			exit()

		pg.init()
		self.screen = pg.display.set_mode(self.settings["app_size"])
		self.font = pg.font.Font(self.settings["app_font"])
		pg.display.set_caption("2D Tile Editor")
		self.clock = pg.time.Clock()
		self.frame = Frame(self, [1000, 800], 0, 0, "#010c0e", "white", 3, 20)
		self.toggle_frame = RightClickFrame(self.frame, [200, 300], "white", "gray", 3, 10)

		self.btn = Button(parent = self.toggle_frame, width = 0.8, height = 0.2, x = 0.1, y = 0.03, text = "This is a button", fg = "blue", bg = "gray", hover_clr = "red", font = self.font, bd_width = 2, bd_clr = "black", bd_radius = 10)

		# frame events handler vars
		self.frames_elapsed = 0
		self.max_frames_elapsed = 10e5

	def load_data(self):
		self.settings = None
		try:
			with open("settings.json", "r") as f:
				self.settings = load(f)
		except FileNotFoundError as e:
			pass

	def run(self):
		while True:
			mouse_pos = pg.mouse.get_pos()

			for event in pg.event.get():
				if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
					pg.quit()
					exit()
				if event.type == pg.MOUSEBUTTONDOWN:
					if event.button == 3:
						self.toggle_frame.update(mouse_pos[0], mouse_pos[1])
					
						if not self.toggle_frame.rect.collidepoint(pg.mouse.get_pos()):
							self.toggle_frame.update()

			# don't change this pls
			self.frames_elapsed += 1
			self.frames_elapsed %= self.max_frames_elapsed

			# clearing the screen
			self.screen.fill((0, 0, 0))
			self.frame.draw(self.screen)
			self.toggle_frame.draw(self.screen)

			self.btn.update()
			self.btn.draw(self.screen)


			pg.display.update()
			self.clock.tick(self.settings["fps"])


if __name__ == "__main__":
	a = App()
	a.run()