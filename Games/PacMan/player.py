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
		# for debugging
		# pg.draw.rect(self.display, 'red', (map_pos[0], map_pos[1], TILE_SIZE, TILE_SIZE))

	def update(self):
		self.take_input()
		# self.draw_available()
		self.apply_input()
		self.animate()
		self.move()

	# drawing available squares for debugging 
	def draw_available(self):
		available = self.game.collisions_manager.get_available_direction(self.get_tile_pos())
		x1, y1 = self.get_tile_pos()
		x1, y1 = x1 * TILE_SIZE + self.game.offset_x, y1 * TILE_SIZE + self.game.offset_y
		if "up" in available:
			pg.draw.rect(self.display, "green", (x1, y1 - TILE_SIZE, TILE_SIZE, TILE_SIZE))
		if "down" in available:
			pg.draw.rect(self.display, "green", (x1, y1 + TILE_SIZE, TILE_SIZE, TILE_SIZE))
		if "left" in available:
			pg.draw.rect(self.display, "green", (x1 - TILE_SIZE, y1, TILE_SIZE, TILE_SIZE))
		if "right" in available:
			pg.draw.rect(self.display, "green", (x1 + TILE_SIZE, y1, TILE_SIZE, TILE_SIZE))

	def apply_input(self):
		if not self.next_direction: return
		available = self.game.collisions_manager.get_available_direction(self.get_tile_pos())
		if OPP_MAP[self.direction] in available: available.remove(OPP_MAP[self.direction])
		if not available: return
		if self.next_direction not in available: return

		vector = 1
		if self.next_direction in VECTOR_MAP["horizontal"]:
			vector = 0

		if abs(self.pos[vector] % 1) < 0.05:
			self.direction = self.next_direction
			self.next_direction = ""
			self.pos[vector] = round(self.pos[vector])
	
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
		for keys_ in KEY_MAP:
			for key in keys_:
				if keys[key] and KEY_MAP[keys_] != OPP_MAP[self.direction]:
					self.next_direction = KEY_MAP[keys_]

	# returns the tile position of the top left tile since int floors floating point values
	def get_tile_pos(self):
		x = self.pos[0] if abs(self.pos[0] % 1) < 0.5 else self.pos[0] + 1
		y = self.pos[1] if abs(self.pos[1] % 1) < 0.5 else self.pos[1] + 1
		return int(x), int(y)

	# return the map positon of the top left point of the player
	def get_map_pos(self):
		return self.pos[0] * TILE_SIZE + self.game.offset_x, self.pos[1] * TILE_SIZE + self.game.offset_y

