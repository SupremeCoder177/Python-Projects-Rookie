# this module contains all kinds of frame widget

# NOTE : these widgets are made very similarly to tkinter system
# 		 or java.swing module if you will, i.e there is a lot of 
# 		 inheritance stuff going on, every widget will need to have a parent
# 		 of course it is just to get the coding easier

import pygame as pg
from typing import List
from widgets.default import Widget


# a simple container frame
class Frame(Widget):

	def __init__(self, parent, size : List[int], x : int, y : int, bg : str, bd_clr : str, bd_width : int, bd_radius : int):
		super().__init__()
		self.parent = parent
		self.bg = bg
		self.rect = pg.Rect((x, y, size[0], size[1]))
		self.bd_radius = bd_radius
		self.bd_clr = bd_clr
		self.bd_width = bd_width
		self.children = []

	# draws the frame
	def draw(self, surface : pg.Surface):	
		pg.draw.rect(surface, self.bg, self.rect, border_radius = self.bd_radius)
		if self.bd_radius > 0:
			pg.draw.rect(surface, self.bd_clr, self.rect, self.bd_width, self.bd_radius)

	# sometimes you need to update the frame, but only for frames which have some changes
	def update(self):
		pass

	# adds a widget to its children, the widget is the object's id
	def add_child(self, widget : int):
		if widget not in self.children: self.children.append(widget)

	# deletes a specific child from the children list
	def delete_child(self, widget : int):
		if widget in self.children: self.children.remove(widget)


# this frame should only be one per screen, because well if you have multiple then it will 
# be kinda weird when you right click
class RightClickFrame(Frame):

	def __init__(self, parent, size : List[int], bg : str, bd_clr : str, bd_width : int, bd_radius : int):
		super().__init__(parent, size, 0, 0, bg, bd_clr, bd_width, bd_radius)

	def draw(self, surface : pg.Surface):
		if not self.shown: return
		super().draw(surface)

	def update(self, x = 0, y = 0):
		super().update()
		self.shown = not self.shown
		self.rect.x = x
		self.rect.y = y
		



		