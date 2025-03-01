# widgets

import pygame as pg


class Button:

	def __init__(self, surf, text, bg, fg, hover, font, x, y, width, height):
		self.surf = surf
		self.text = text
		self.bg = bg
		self.fg = fg
		self.curr_color = bg
		self.font = font
		self.hvr_clr = hover
		self.rect = pg.Rect(x, y, width, height)

	def render(self):
		pg.draw.rect(self.surf, self.curr_color, self.rect, border_radius = 20)
		text_surf = self.font.render(self.text, False, self.fg)
		x = ((self.rect.width - text_surf.get_width()) // 2) + self.rect.x
		y = ((self.rect.height - text_surf.get_height()) // 2) + self.rect.y
		text_rect = text_surf.get_rect(topleft = (x, y))
		self.surf.blit(text_surf, text_rect)

	def update(self):
		if self.rect.collidepoint(pg.mouse.get_pos()):
			self.curr_color = self.hvr_clr
		else:
			self.curr_color = self.bg

	def clicked(self, event):
		return event.type == pg.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)