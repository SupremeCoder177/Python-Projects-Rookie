# this module contains all the widgets

import pygame as pg


# simpel oval button
class Button:

	def __init__(self, text : str, font : pg.font.Font, foreground  : str, x : int, y : int, width : int, height : int, color : str, hover_clr : str, border_radius : int):
		self.font = font
		self.text = text
		self.color = color
		self.hover_clr = hover_clr
		self.hovering = False
		self.fg = foreground
		self.rect = pg.Rect(x, y, width, height)
		self.br = border_radius

	def draw(self, screen : pg.Surface):
		pg.draw.rect(screen, self.color if not self.hovering else self.hover_clr, self.rect, self.rect.width, self.br)
		text_surf = self.font.render(self.text, False, self.fg)
		x = ((self.rect.width - text_surf.get_width()) // 2)  + self.rect.x
		y = ((self.rect.height - text_surf.get_height()) // 2) + self.rect.y
		text_rect = text_surf.get_rect(topleft = (x, y))
		screen.blit(text_surf, text_rect)

	def update(self):
		self.hovering = self.rect.collidepoint(pg.mouse.get_pos())



