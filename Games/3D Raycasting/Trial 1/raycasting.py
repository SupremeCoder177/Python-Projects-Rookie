# raycasting engine

import pygame as pg
from math import *
from settings import *

class RayCast:

	def __init__(self, game):
		self.player = game.player
		self.display = game.screen
		self.map = game.map
		self.depths = []

	# draws them too fyi
	# I didn't come up with method btw saw it on a vid on youtube
	# its really laggy so I don't recommend using it, also I am sure I messed up the logic somewhere
	def cast_rays(self):
		player_angle = self.player.angle
		self.depths.clear()
		ray_angle = player_angle - PLAYER_HALF_FOV + 1e-4

		px, py = self.player.pos
		ox, oy = self.player.tile_pos()
		for i in range(NUM_RAYS):
			sin_a = sin(ray_angle)
			cos_a = cos(ray_angle)

			# horizontal wall collision with rays

			y_hor, dy = (oy + 1, 1) if sin_a > 0 else (oy - 1e-4, -1)

			depth_hor = y_hor / sin_a
			x_hor = depth_hor * cos_a

			depth_delta = dy / sin_a
			dx = cos_a * depth_delta

			for i in range(MAX_DEPTH):
				tile_hor = int(x_hor), int(y_hor)
				if self.map.is_occupied(tile_hor):
					break
				x_hor += dx
				y_hor += dy
				depth_hor += depth_delta

			# vertical wall collision with rays

			x_vert, dx = (ox + 1, 1) if cos_a > 0 else (ox - 1e-4, -1)

			depth_vert = (x_vert - px) / cos_a
			y_vert = depth_vert * (sin_a + py)

			depth_delta = dx / cos_a
			dy = sin_a * depth_delta

			for i in range(MAX_DEPTH):
				tile_vert = int(x_vert), int(y_vert)
				if self.map.is_occupied(tile_vert):
					break
				x_vert += dx
				y_vert += dy 
				depth_vert += depth_delta

			depth = depth_hor if depth_hor < depth_vert else depth_vert
			self.depths.append(depth)

			ray_angle += RAY_INC_ANGLE

	def player_direction_ray(self):
		sin_a = sin(self.player.angle)
		cos_a = cos(self.player.angle)

		px, py = self.player.pos
		ox, oy = self.player.tile_pos()

		y_hor, dy = (oy + 1, 1) if sin_a > 0 else (oy - 1e-4, -1)
		depth_hor = y_hor / sin_a if sin_a != 0 else 1 - (px - ox)
		x_hor = depth_hor * cos_a
		depth_delta = dy / sin_a if sin_a != 0 else 1
		dx = cos_a * depth_delta

		for i in range(MAX_DEPTH):
			tile_hor = int(x_hor), int(y_hor)
			if tile_hor in self.map.world_map:
				break
			x_hor += dx
			y_hor += dy
			depth_hor += depth_delta

		x_vert, dx = (ox + 1, 1) if cos_a > 0 else (ox - 1e-4, -1)
		depth_vert = (x_vert - px) / cos_a if cos_a != 0 else 1 - (py - oy)
		y_vert = depth_vert * (sin_a + py)
		depth_delta = dx / cos_a if cos_a != 0 else 1
		dy = sin_a * depth_delta

		for i in range(MAX_DEPTH):
			tile_vert = int(x_vert), int(y_vert)
			if self.map.is_occupied(tile_vert):
				break
			x_vert += dx
			y_vert += dy 
			depth_vert += depth_delta

		depth = depth_hor if depth_hor < depth_vert else depth_vert
		x = (px + depth * cos_a) * TILE_SIZE
		y = (py + depth * sin_a) * TILE_SIZE
		pg.draw.line(self.display, "yellow", self.player.map_pos(), (x, y))

	def get_collisions(self):
		self.depths.clear()
		px, py = self.player.pos
		ray_angle = self.player.angle - PLAYER_HALF_FOV + 1e-5

		for i in range(NUM_RAYS):
			dx = cos(ray_angle)
			dy = sin(ray_angle)
			x, y = px, py
			depth = 0

			for j in range(MAX_DEPTH):
				if (int(x + dx), int(y + dy)) in self.map.world_map:
					break
				depth += 1
				x += dx
				y += dy

			self.depths.append(depth)
			ray_angle += RAY_INC_ANGLE

	def draw(self):
		# ray_angle = self.player.angle - PLAYER_HALF_FOV + 1e-5
		# for depth in self.depths:
		# 	player_pos = self.player.map_pos()
		# 	x = (player_pos[0] + depth * cos(ray_angle)) * TILE_SIZE
		# 	y =( player_pos[1] + depth * sin(ray_angle)) * TILE_SIZE
		# 	pg.draw.line(self.display, "yellow", self.player.map_pos(), (x, y), 2)
		# 	ray_angle += RAY_INC_ANGLE

		pass

	# this method I came up with and enhanced with chatGPT and it works, apprently its called Ray Marching not Ray Casting
	def ray_cast_method_2(self):
		px, py = self.player.pos

		ray_angle = self.player.angle - PLAYER_HALF_FOV + 1e-4
		for i in range(NUM_RAYS):
			cos_a = cos(ray_angle)
			sin_a = sin(ray_angle)
			depth = 0
			step_size = 0.02

			while depth < MAX_DEPTH:
				x = px + cos_a * depth
				y = py + sin_a * depth

				if (int(x), int(y)) in self.map.world_map:
					break
				depth += step_size

			start = (px * TILE_SIZE, py * TILE_SIZE)
			end = ((px + cos_a * depth) * TILE_SIZE, (py + sin_a * depth) * TILE_SIZE)

			# drawing rays for debugging
			# pg.draw.line(self.display, 'yellow', start, end)

			# 3D projection
			proj_height = SCREEN_DIST / (depth + 1e-6)
			color = [255 / (1 + depth ** 5 * 2e-6)] * 3
			pg.draw.rect(self.display, color, 
				(i * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height))
			ray_angle += RAY_INC_ANGLE

	def update(self):
		self.ray_cast_method_2()
