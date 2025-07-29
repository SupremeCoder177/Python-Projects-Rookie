# Graphics Loader for PacMan

import pygame as pg
from os import listdir
from settings import *


class Load:

	def __init__(self):
		self.sprites_total = 0
		self.enemies = {}


		# up, down, right, left represent the sprite tpyes which represent those animations for enemies
		self.enemy_anims = {"red" : {"right" : [],
									 "left" : [],
									 "down" : [],
									 "up" : []},
		"blue" : {					"right" : [],
									 "left" : [],
									 "down" : [],
									 "up" : []},
		"green" : 					{"right" : [],
									 "left" : [],
									 "down" : [],
									 "up" : []},
		"cyan" : 					{"right" : [],
									 "left" : [],
									 "down" : [],
									 "up" : []}}
		self.sprites = dict()
		self.load_wall_images()
		self.load_player_images()
		self.load_enemy_images()

	# loads the png frames of each wall type from the graphics folder in current working directory
	def load_wall_images(self):
		image = pg.image.load("graphics/walls.png").convert_alpha()
		for i in range(image.get_width() // WALL_WIDTH):
			for j in range(image.get_height() // WALL_HEGIHT):
				temp = pg.Surface((WALL_WIDTH, WALL_HEGIHT))
				temp.blit(image, (0, 0), (i * WALL_WIDTH, j * WALL_HEGIHT, WALL_WIDTH, WALL_HEGIHT))
				temp = pg.transform.scale(temp, (WALL_MAP_WIDTH, WALL_MAP_HEIGHT))
				self.sprites[self.sprites_total] = {"wall" + str(self.sprites_total + 1) : temp}
				self.sprites_total += 1

	def load_player_images(self):
		image = pg.image.load("graphics/player.png").convert_alpha()
		for i in range(image.get_width() // PLAYER_WIDTH):
			for j in range(image.get_height() // PLAYER_HEIGHT):
				temp = pg.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
				temp.blit(image, (0, 0), (i * PLAYER_WIDTH, j * PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT))
				self.sprites[self.sprites_total] = {"player" + str(i) : temp}
				self.sprites_total += 1

	def load_enemy_images(self):
		images = [pg.image.load(f"graphics/{image}") for image in listdir("graphics/") if image.startswith("enemy")]
		count = 0

		# these variables depend on the files
		# in the grpahics folder, and the way
		# the loop access each sprite
		anim_index = {
		0 : "right",
		1 : 'left',
		2 : "down",
		3 : "up"
		}
		enemey_color_index = {
		0 : "red",
		1 : "blue",
		2 : "green",
		3 : "cyan"
		}

		enemey_color_index_count = 0
		for image in images:
			types = []
			anim_index_count = 0
			for i in range(image.get_width() // ENEMY_WIDTH):
				anims = []
				for j in range(image.get_height() // ENEMY_HEIGHT):
					temp = pg.Surface((PLAYER_WIDTH, ENEMY_HEIGHT))
					temp.blit(image, (0, 0), (i * ENEMY_WIDTH, j * ENEMY_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT))
					self.sprites[self.sprites_total] = {"enemy" + str(count) : temp}
					self.sprites_total += 1
					types.append("enemy" + str(count))
					anims.append("enemy" + str(count))
					count += 1
				self.enemy_anims[enemey_color_index[enemey_color_index_count]][anim_index[anim_index_count]] = anims
				anim_index_count += 1
			self.enemies[tuple(types)] = enemey_color_index[enemey_color_index_count]
			enemey_color_index_count += 1
