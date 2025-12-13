# this module defines the main loading screen of the app

import pygame as pg
from widgets.screen import Screen
from widgets import frame
from widgets.buttons import Button

class LoadingScreen(Screen):

	def __init__(self, game, settings):
		super().__init__(game, settings)

		# the main container for all widgets
		self.main_frame = frame.Frame(self, self.settings["main_size"], self.settings["main_x"], self.settings["main_y"], self.settings["main_bg"], self.settings["main_bd_clr"], self.settings["main_bd_width"], self.settings["main_bd_radius"])
		self.main_frame.shown = True
		self.add(id(self.main_frame), self.main_frame)
