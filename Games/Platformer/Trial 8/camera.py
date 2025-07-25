# Camera

import pygame as pg

class Camera:

	def __init__(self, game, player):
		self.game = game
		self.player = player

	def change_offset_centered(self):
		window_width, window_height = pg.display.get_window_size()
		self.game.offset_x = -self.player.pos[0] + (self.player.width // 2) + (window_width // 2) - self.game.settings["tile_size"]
		self.game.offset_y = -self.player.pos[1] + (self.player.height // 2) + (window_height // 2)

	def change_offset_contained(self):
		window_width, window_height = pg.display.get_window_size()

		# horizontal containment
		if self.player.pos[0] + (self.player.width // 2) + self.game.offset_x > (window_width // 2) + (2 * self.game.settings["tile_size"]) and (pg.K_d in self.game.keys_held or pg.K_RIGHT in self.game.keys_held):
			self.game.offset_x += -self.game.settings["player_move_speed"]
		if self.player.pos[0] + (self.player.width // 2) + self.game.offset_x < (window_width // 2) - (3 * self.game.settings["tile_size"]) and (pg.K_a in self.game.keys_held or pg.K_LEFT in self.game.keys_held):
			self.game.offset_x += self.game.settings["player_move_speed"]

		# vertical containment
		if self.player.pos[1] + (self.player.height // 2) + self.game.offset_y > (window_height // 2) + (3 * self.game.settings["tile_size"]) and self.player.y_collide == 0:
			self.game.offset_y += self.player.gravity
		if self.player.pos[1] + (self.player.height // 2) + self.game.offset_y < (window_height // 2) and self.player.y_collide == 0:
			self.game.offset_y -= self.player.gravity

	def update(self):
		self.change_offset_centered()
		#self.change_offset_contained()