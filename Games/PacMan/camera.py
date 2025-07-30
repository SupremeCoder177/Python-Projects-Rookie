# camera

import pygame as pg
from settings import *

class Camera:

	def __init__(self, game):
		self.game = game

	# produces weird result so don't use this one
	def change_offset_centered(self):
		width, height = pg.display.get_window_size()
		px, py = self.game.player.get_map_pos()
		p_width, p_height = self.game.player.curr_surf.get_size()
		self.game.offset_x = int(-px + (p_width // 2) + (width // 2))
		self.game.offset_y = int(-py + (p_height // 2) + (height // 2))

	def change_offset_contained(self):
		px, py = self.game.player.get_map_pos()
		width, height = pg.display.get_window_size()
		p_width, p_height = self.game.player.curr_surf.get_size()
		SPEED = PLAYER_MOVE_SPEED * TILE_SIZE * self.game.delta_time
		if px + p_width > (width / 2) + (2 * TILE_SIZE):
			self.game.offset_x -= SPEED
		if px < (width / 2) - (3 * TILE_SIZE):
			self.game.offset_x += SPEED
		if py > (height / 2):
			self.game.offset_y -= SPEED
		if py < (height / 2) - (2 * TILE_SIZE):
			self.game.offset_y += SPEED
