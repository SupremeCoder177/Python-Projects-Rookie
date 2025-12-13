# app screen module

# This module defines a single containerized widget group which the main game loop
# can draw, along with all its widgets that it contains

from widgets import *
from widgets.default import Widget
import pygame as pg

# the screen class is not a widget, rather a way to store and
# organize other widgets, including containers like frames.
# it handles the drawing and updating logic, and also triggers
# code based on user input
# the widgets it makes will be preset in their appearance according to the settings passed into it
class Screen:

	def __init__(self, game, settings):
		self.game = game
		self.settings = settings
		self.widgets = dict()

	# deletes the specified widget from the screen, along with all its children
	def delete(self, widget : int):
		if widget in self.widgets: del self.widgets[widget]

	# adds a widget to the widgets dics
	def add(self, widget : int, ref : Widget):
		if not widget in self.widgets: self.widgets[widget] = ref

	# draws all the widgets on the given surfac
	def draw(self, surface : pg.Surface):
		for id_ in self.widgets.keys():
			if self.widgets[id_].shown:
				self.widgets[id_].draw(surface)
