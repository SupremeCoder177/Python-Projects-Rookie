# coin manager 

import pygame as pg
from settings import *

class Coins:

	def __init__(self, game):
		self.frames = game.graphics.coins
		self.anim_index = 0.0
		self.display = game.screen
		self.game = game
		self.positions = game.level_loader.data["coin_positions"]

	def draw_coins(self):
		# the reason we add half width and height to coin is because they have been shrunk half
		# their original size, so they appear to be in the top left cornet of the tile and not 
		# in the center
		for position in self.positions:
			map_pos = position[0] * TILE_SIZE + self.game.offset_x + ((COIN_WIDTH  - COIN_MAP_WIDTH) / 2), position[1] * TILE_SIZE + self.game.offset_y + ((COIN_HEIGHT - COIN_MAP_HEIGHT) / 2)
			surf = self.frames[int(self.anim_index)]
			self.display.blit(surf, map_pos)

	def update(self):
		self.animate()
		self.check_eaten()

	def animate(self):
		self.anim_index += COIN_ANIM_SPEED * self.game.delta_time 
		self.anim_index %= len(self.frames)

	def check_eaten(self):
		player_tile_pos = list(self.game.player.get_tile_pos())
		if player_tile_pos in self.positions:
			self.positions.remove(player_tile_pos)
