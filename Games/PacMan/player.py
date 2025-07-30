# Player

import pygame as pg
from settings import *

class Player:

	def __init__(self, game):
		self.display = game.screen
		self.game = game
		self.frames = game.graphics.player_frames
		self.anim_index = 0.0
		self.pos = game.level_loader.data["player_pos"]
		self.direction = "right"
		self.next_direction = ""
		self.curr_surf = self.frames[self.direction][int(self.anim_index)]
		self.directional_speed_map = {
			"right" : [PLAYER_MOVE_SPEED, 0],
			"left" : [-PLAYER_MOVE_SPEED, 0],
			"up" : [0, -PLAYER_MOVE_SPEED],
			"down" : [0, PLAYER_MOVE_SPEED]
		}

	def draw(self):
		self.curr_surf = self.frames[self.direction][int(self.anim_index)]
		map_pos = self.pos[0] * TILE_SIZE + self.game.offset_x + (PLAYER_WIDTH / 2) - (PLAYER_MAP_WIDTH / 2), self.pos[1] * TILE_SIZE + self.game.offset_y + (PLAYER_HEIGHT / 2) - (PLAYER_MAP_HEIGHT / 2)
		self.display.blit(self.curr_surf, map_pos)

	def update(self):
		self.take_input()
		self.apply_input()
		self.animate()
		self.move()

	def apply_input(self):
		if not self.next_direction: return
		available = self.game.collisions_manager.get_available_direction(self.get_tile_pos())
		if OPP_MAP[self.direction] in available: available.remove(OPP_MAP[self.direction])
		if self.next_direction not in available: return

		vector = 0
		for direction_ in VECTOR_MAP:
			if self.next_direction in VECTOR_MAP[direction_]:
				vector = 0 if VECTOR_MAP[direction_] == "horizontal" else 1
				break
		if self.pos[vector] % 1 < 0.1:
			self.direction = self.next_direction
			self.next_direction = ""
			self.pos[vector] = self.pos[vector] + (self.pos[vector] % 1)
	
	def animate(self):
		self.anim_index += PLAYER_ANIM_SPEED * self.game.delta_time
		self.anim_index %= len(self.frames[self.direction])

	def move(self):
		dx = self.directional_speed_map[self.direction][0] * self.game.delta_time
		dy = self.directional_speed_map[self.direction][1] * self.game.delta_time
		self.pos[0] += dx
		self.pos[1] += dy

	def take_input(self):
		keys = pg.key.get_pressed()

		if keys[pg.K_a] or keys[pg.K_LEFT]:
			self.next_direction = "left"
		if keys[pg.K_d] or keys[pg.K_RIGHT]:
			self.next_direction = "right"
		if keys[pg.K_s] or keys[pg.K_DOWN]:
			self.next_direction = "down"
		if keys[pg.K_w] or keys[pg.K_UP]:
			self.next_direction = "up"

	# returns the tile position of the top left tile since int floors floating point values
	def get_tile_pos(self):
		return int(self.pos[0]), int(self.pos[1])

	# return the map positon of the top left point of the player
	def get_map_pos(self):
		return self.pos[0] * TILE_SIZE + self.game.offset_x, self.pos[1] * TILE_SIZE + self.game.offset_y

