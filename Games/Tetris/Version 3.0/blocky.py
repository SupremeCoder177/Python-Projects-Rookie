# this module defines blocky (the screen pet)

import pygame as pg
from animations import Animation


class Blocky:

	def __init__(self, game, x : int, y : int, tile_size : int):
		self.game = game
		self.x = x
		self.y = y
		self.tile_size = tile_size

		# if you want to make custome animations then remember to change this path pls
		anim_path = "Images/Blocky Animations/"
		anim_duration = 15 # frames for each sprite

		# loading all the animations

		# state and animation mapping
		self.anim_map = {
			"idle" : Animation(anim_path + "blocky_idle.png", 32, anim_duration)
		}

		# animation settings

		# state
		self.state = "idle"
		self.changed_state = True

	def draw(self):
		if self.changed_state:
			self.anim_map[self.state].reset()
			self.changed_state = False

		self.anim_map[self.state].update(self.game.frames_elapsed)
		self.anim_map[self.state].draw(self.x, self.y, self.game.screen, self.tile_size)

	def set_state(self, state : str):
		self.state = state if state in self.anim_map else self.state
		self.changed_state = True