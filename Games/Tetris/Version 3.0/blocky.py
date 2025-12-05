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
		self.idle_anim = Animation(anim_path + "blocky_idle.png", 32, anim_duration)

		# animation settings
		self.anims = [self.idle_anim]
		self.anim_index = 0

		# state
		self.state = "idle"

		# state and animation mapping
		self.anim_map = {
			"idle" : 0
		}

		self.anims[self.anim_index].reset()

	def draw(self):
		self.anims[self.anim_index].update(self.game.frames_elapsed)
		self.anims[self.anim_index].draw(self.x, self.y, self.game.screen, self.tile_size)
