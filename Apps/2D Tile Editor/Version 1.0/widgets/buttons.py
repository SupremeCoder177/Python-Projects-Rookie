# this module defines a button widget


import pygame as pg
from widgets.frame import Frame
from widgets.default import Widget


# simple button with a text and hover effect and simple border
class Button(Widget):

	def __init__(self, parent : Frame, width : float, height : float, x : float, y : float, text : str, font : pg.font.Font, fg : str, bg : str, hover_clr : str, bd_width = 0, bd_clr = "white", bd_radius = 0, commands = lambda: print("Button was clicked")):
		super().__init__()
		self.parent = parent
		self.bg = bg
		self.x = x
		self.y = y
		self.rect = pg.Rect((0, 0, parent.rect.width * width, parent.rect.height * height))
		self.bd_radius = bd_radius	
		self.bd_width = bd_width
		self.hover_clr = hover_clr
		self.bd_clr = bd_clr
		self.text_surf = font.render(text, False, fg)
		self.text_rect = self.text_surf.get_rect()
		self.hovering = False

	# this function dynamically positions the widget
	def calc_positions(self):

		# updating the rect position
		dx = self.parent.rect.x + (self.parent.rect.width * self.x)
		dy = self.parent.rect.y + (self.parent.rect.height * self.y)

		self.rect.x = dx
		self.rect.y = dy

		# updating the text position based on self.rect position
		tdx = (self.rect.width - self.text_rect.width) / 2 + self.rect.x
		tdy = (self.rect.height - self.text_rect.height) / 2 + self.rect.y

		self.text_rect.x = tdx
		self.text_rect.y = tdy

	def draw(self, surface : pg.Surface):
		if not self.parent.shown: return

		self.calc_positions()

		# drawing the body of the button
		pg.draw.rect(surface, self.bg if not self.hovering else self.hover_clr, self.rect, border_radius = self.bd_radius)

		if self.bd_width > 0:
			pg.draw.rect(surface, self.bd_clr, self.rect, self.bd_width, self.bd_radius)

		# rendering the text
		surface.blit(self.text_surf, self.text_rect)

	def update(self):
		self.hovering = self.rect.collidepoint(pg.mouse.get_pos())