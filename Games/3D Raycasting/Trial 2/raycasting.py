# Raycasting 

import pygame as pg
from math import *
from settings import *

class RayCasting:

	def __init__(self, game):
		self.display = game.screen
		self.player = game.player
		self.map = game.map

	# traditional grid raycasting technique
	def cast_rays(self):
		ox, oy = self.player.tile_pos() # absolute tile position of the player
		px, py = self.player.pos # tile position
		ray_angle = self.player.angle - HALF_PLAYER_FOV + 1e-5

		for i in range(NUM_RAYS):
			sin_a = sin(ray_angle)
			cos_a = cos(ray_angle)

			# horizontal 
			y_hor, dy = (oy + 1, 1) if sin_a > 0 else (oy - 1e-5, -1)
			depth_hor = (y_hor - py) / sin_a
			x_hor = px + depth_hor * cos_a
			depth_delta = dy / sin_a
			dx = cos_a * depth_delta

			while depth_hor < MAX_DEPTH:
				tile_x = int(x_hor)
				tile_y = int(y_hor)
				if (tile_x, tile_y) in self.map.world_map:
					break
				x_hor += dx
				y_hor += dy
				depth_hor += depth_delta

			# verticlas
			x_vert, dx = (ox + 1, 1) if cos_a > 0 else (ox - 1e-5, -1)
			depth_vert = (x_vert - px) / cos_a
			y_vert = py + depth_vert * sin_a
			depth_delta = dx / cos_a
			dy = sin_a * depth_delta

			while depth_vert < MAX_DEPTH:
				tile_x = int(x_vert)
				tile_y = int(y_vert)
				if (tile_x, tile_y) in self.map.world_map:
					break
				x_vert += dx
				y_vert += dy
				depth_vert += depth_delta

			depth = depth_vert if depth_vert < depth_hor else depth_hor

			# drawing rays for debugging
			end = (px + depth * cos_a) * TILE_SIZE, (py + depth * sin_a) * TILE_SIZE
			pg.draw.line(self.display, 'yellow', self.player.map_pos(), end)

			ray_angle += DELTA_ANGLE

	# ray marching technique 
	def march_rays(self):
		ray_angle = self.player.angle - HALF_PLAYER_FOV + 1e-5
		max_depth = MAX_DEPTH * TILE_SIZE
		for i in range(NUM_RAYS):
			curr_pos = list(self.player.map_pos())
			step = 1 # pixels
			depth = 0
			cos_a = cos(ray_angle)
			sin_a = sin(ray_angle)
			while depth < max_depth:
				curr_pos[0] += step * cos_a
				curr_pos[1] += step * sin_a
				depth += 1
				
				tile_x = int(curr_pos[0] // TILE_SIZE)
				tile_y = int(curr_pos[1] // TILE_SIZE)
				if (tile_x, tile_y) in self.map.world_map:
					break

			pg.draw.line(self.display, 'yellow', self.player.map_pos(), curr_pos)
			ray_angle += DELTA_ANGLE






