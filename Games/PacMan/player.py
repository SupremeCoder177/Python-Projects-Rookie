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
		self.curr_surf = self.frames[self.direction][int(self.anim_index)]
		self.direction_map = {
			"right" : [PLAYER_MOVE_SPEED, 0],
			"left" : [-PLAYER_MOVE_SPEED, 0],
			"up" : [0, -PLAYER_MOVE_SPEED],
			"down" : [0, PLAYER_MOVE_SPEED]
		}
		self.opp_map = {
		"right" : "left",
		"left" : "right",
		"up" : "down",
		"down" : "up"
		}

	def draw(self):
		self.curr_surf = self.frames[self.direction][int(self.anim_index)]
		map_pos = self.pos[0] * TILE_SIZE + self.game.offset_x, self.pos[1] * TILE_SIZE + self.game.offset_y
		self.display.blit(self.curr_surf, map_pos)

	def update(self):
		self.move()
		self.check_collision_enemy()
		self.take_input()
		self.animate()

	def check_collision_wall(self, dx, dy):
		px, py = self.get_tile_pos()
		x1, y1 = 0, 0
		x2, y2 = 0, 0
		if self.direction == "left" or self.direction == "up":
			x1, y1 = px, py
			x2, y2 = px + 1, py
		if self.direction == "right":
			x1, y1 = px + 1, py
			x2, y2 = px + 1, py + 1
		if self.direction == "down":
			x1, y1 = px, py + 1
			x2, y2 = px + 1, py + 1

		if not self.is_blocked(x1 + dx, y1 + dy):
			self.pos[0] += dx
			self.pos[1] += dy

	def check_collision_enemy(self):
		pass

	def take_input(self):
		keys = pg.key.get_pressed()

		if keys[pg.K_a] or keys[pg.K_LEFT]:
			self.check_direction("left")
		if keys[pg.K_d] or keys[pg.K_RIGHT]:
			self.check_direction("right")
		if keys[pg.K_w] or keys[pg.K_UP]:
			self.check_direction("up")
		if keys[pg.K_s] or keys[pg.K_DOWN]:
			self.check_direction("down")

	def animate(self):
		self.anim_index += PLAYER_ANIM_SPEED * self.game.delta_time
		self.anim_index %= len(self.frames[self.direction])

	def move(self):
		dx = self.direction_map[self.direction][0] * self.game.delta_time
		dy = self.direction_map[self.direction][1] * self.game.delta_time
		self.check_collision_wall(dx, dy)

	def get_tile_pos(self):
		return int(self.pos[0]), int(self.pos[1])

	def get_map_pos(self):
		return self.pos[0] * TILE_SIZE + self.game.offset_x, self.pos[1] * TILE_SIZE + self.game.offset_y

	def is_blocked(self, x, y):
		return (int(x), int(y)) in self.game.level_loader.world_map

	def check_direction(self, direction):
		if self.opp_map[self.direction] == direction: return
		if self.direction == direction: return

		tile_pos = self.get_tile_pos()
		upper_tile = (tile_pos[0], tile_pos[1] - 1)
		lower_tile = (tile_pos[0], tile_pos[1] + 1)
		left_tile = (tile_pos[0] - 1, tile_pos[1])
		right_tile = (tile_pos[0] + 1, tile_pos[1])

		if direction == "left" and left_tile not in self.game.level_loader.world_map:
			self.direction = "left"
		if direction == "right" and right_tile not in self.game.level_loader.world_map:
			self.direction = "right"
		if direction == "up" and upper_tile not in self.game.level_loader.world_map:
			self.direction = "up"
		if direction == "down" and lower_tile not in self.game.level_loader.world_map:
			self.direction = "down"






