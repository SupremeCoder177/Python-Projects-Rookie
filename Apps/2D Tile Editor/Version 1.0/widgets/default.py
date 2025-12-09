# all widgets have a draw method and will have a rect attribute

# the coordinates of all non-container widgets will be in relative coordinates to accomodate for different
# parent's specific size

# Container widgets are as follows :
# (i) frame

# Non container widgets are as follows
# (i) Labels
# (ii) Buttons
# (iii) Slider
# (iv) Menu
# (v) Input fields


# All widgets will respond to events if they are actively selected by the user
# this will simply be done using a selected state variable

import pygame as pg


# all widgets will essentially be contained inside a rect
# as for the specific widget the no. of rects and their shape will differ
# consider this rect as a div around the widget
class Widget:

	def __init__(self):
		self.rect = None

	# this function will handle the rendering
	def draw(self):
		pass

	# this function will handle all the events
	def update(self):
		pass