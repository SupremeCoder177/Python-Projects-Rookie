# Enemy Manager

import pygame as pg
from settings import *
from random import choice

class EnemyManager:

	def __init__(self, game):
		self.display = game.screen
		self.game = game
		self.enemy_info = game.level_loader.data["enemy_info"]
		self.enemy_category = game.graphics.enemies
		self.enemy_anims = game.graphics.enemy_anims
		self.anim_index = 0.0
		directions_ = ["right", "down", "left", "up"]
		self.directions = []
		self.collided_ones = []

		# settings random direction movement for all enemies
		for i in range(len(self.enemy_info)):
			self.directions.append(choice(directions_))

		self.directional_speed_map = {
			"up" : [0, -ENEMY_MOVE_SPEED],
			"down" : [0, ENEMY_MOVE_SPEED],
			"left" : [-ENEMY_MOVE_SPEED, 0],
			"right" : [ENEMY_MOVE_SPEED, 0]
		}

	def draw(self):
		count = 0
		for type_, pos in self.enemy_info.items():
			mx, my = pos[0] * TILE_SIZE + self.game.offset_x, pos[1] * TILE_SIZE + self.game.offset_y
			enemy_color = ""
			for temp in self.enemy_category:
				if type_ in temp:
					enemy_color = self.enemy_category[temp]
					break
			surf = self.enemy_anims[enemy_color][self.directions[count]][int(self.anim_index)]
			self.display.blit(surf, (mx, my))
			count += 1

	def update(self):
		self.move()
		self.animate()

	def animate(self):
		self.anim_index += ENEMY_ANIM_SPEED * self.game.delta_time
		self.anim_index %= 4 # though this is a magic number it is based on the no. of frames of animation for the enemy sprites

	def move(self):
		count = 0
		for type_ in self.enemy_info:
			self.enemy_info[type_][0] += self.directional_speed_map[self.directions[count]][0] * self.game.delta_time
			self.enemy_info[type_][1] += self.directional_speed_map[self.directions[count]][1] * self.game.delta_time
			count += 1

	def get_tile_pos(self, type_):
		pos = self.enemy_info[type_]
		return int(pos[0]), int(pos[1])