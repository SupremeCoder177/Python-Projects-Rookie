# camera

from player import *


class Camera:

	def __init__(self, player, map_):
		self.player = player
		self.player_rect = player.player_rect
		self.map = map_

	def update(self):
		self.check_pos()		

	def check_pos(self):
		if self.player_rect.x <= 2 * COL_SIZE and self.player.direction_x[0]:
			self.map.shift(PLAYER_SPEED, 0)
			self.player.player_speed = 0
		elif self.player_rect.x + COL_SIZE >= SCREEN_SIZE[0] - 2 * COL_SIZE and self.player.direction_x[1]:
			self.map.shift(-PLAYER_SPEED, 0)
			self.player.player_speed = 0
		else:
			self.player.player_speed = PLAYER_SPEED
