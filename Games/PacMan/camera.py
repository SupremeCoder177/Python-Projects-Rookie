# camera

import pygame as pg
from settings import *

class Camera:

	def __init__(self, game):
		self.game = game

	def change_offset_centered(self):
		width, height = pg.display.get_window_size()
		px, py = self.game.player.get_map_pos()
		p_width, p_height = self.game.player.curr_surf.get_size()
		self.game.offset_x = int(-px + (p_width // 2) + (width // 2))
		self.game.offset_y = int(-py + (p_height // 2) + (height // 2))