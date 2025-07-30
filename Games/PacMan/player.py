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
		self.change_direction = False
		self.change_to = ""
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
		map_pos = self.pos[0] * TILE_SIZE + self.game.offset_x + (PLAYER_WIDTH / 2) - (PLAYER_MAP_WIDTH / 2), self.pos[1] * TILE_SIZE + self.game.offset_y + (PLAYER_HEIGHT / 2) - (PLAYER_MAP_HEIGHT / 2)
		# for debugging
		self.highlight_player_tiles()
		self.display.blit(self.curr_surf, map_pos)

	def update(self):
		self.animate()
		self.move()
		self.take_input()
		self.check_wall_collision()
		print(self.direction)

	def take_input(self):
		keys = pg.key.get_pressed()

		if keys[pg.K_a] or keys[pg.K_LEFT]:
			self.change_to = "left"
		if keys[pg.K_s] or keys[pg.K_DOWN]:
			self.change_to = "down"
		if keys[pg.K_d] or keys[pg.K_RIGHT]:
			self.change_to = "right"
		if keys[pg.K_w] or keys[pg.K_UP]:
			self.change_to = "up"

	def check_wall_collision(self):
		x1, y1 = self.pos
		x2 = x1 + 1
		y2 = y1 + 1
		points = [(x1, y1), (x1, y2), (x2, y1), (x2, y2)]
		for point in points:
			if self.game.level_loader.is_blocked(point):
				self.change_direction = True
				break
		if self.change_direction:
			dx = self.direction_map[self.direction][0] * self.game.delta_time
			dy = self.direction_map[self.direction][1] * self.game.delta_time	
			self.pos[0] -= dx
			self.pos[1] -= dy
			directions = self.availabel_directions()
			if self.change_to in directions:
				self.direction = self.change_to
				self.change_to = ""
			else:
				if not directions:
					self.direction = self.opp_map[self.direction]
				else:
					self.direction = directions[0]
			self.change_direction = False

	def availabel_directions(self):
		directions = ["up", "down", "left", "right"]
		directions.remove(self.direction)
		directions.remove(self.opp_map[self.direction])
		remove_list = []
		x1, y1 = self.get_tile_pos()
		x2 = x1 + 1
		y2 = y1 + 1

		# checking if the tiles around the player tile are occupied by walls
		if self.game.level_loader.is_blocked((x1, y1)) and self.game.level_loader.is_blocked((x2, y1)): remove_list.append("up")
		if self.game.level_loader.is_blocked((x1, y1)) and self.game.level_loader.is_blocked((x1, y2)): remove_list.append("left")
		if self.game.level_loader.is_blocked((x2, y1)) and self.game.level_loader.is_blocked((x2, y2)): remove_list.append("right")
		if self.game.level_loader.is_blocked((x1, y2)) and self.game.level_loader.is_blocked((x2, y2)): remove_list.append("down")

		for item in remove_list:
			try:
				directions.remove(item)
			except ValueError as e: 
				continue
		return directions

	def animate(self):
		self.anim_index += PLAYER_ANIM_SPEED * self.game.delta_time
		self.anim_index %= len(self.frames[self.direction])

	# to see the tiles around the player for debugging
	def highlight_player_tiles(self):
		map_pos = self.get_map_pos()
		pg.draw.rect(self.display, 'red', (map_pos[0], map_pos[1], TILE_SIZE, TILE_SIZE), 1)

	def move(self):
		dx = self.direction_map[self.direction][0] * self.game.delta_time
		dy = self.direction_map[self.direction][1] * self.game.delta_time
		self.pos[0] += dx
		self.pos[1] += dy

	# returns the tile position of the top left tile since int floors floating point values
	def get_tile_pos(self):
		return int(self.pos[0]), int(self.pos[1])

	# return the map positon of the top left point of the player
	def get_map_pos(self):
		return self.pos[0] * TILE_SIZE + self.game.offset_x, self.pos[1] * TILE_SIZE + self.game.offset_y

