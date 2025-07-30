# Graphics Loader for PacMan

import pygame as pg
from os import listdir
from settings import *

# NOTE : The self.sprites variable is only used by the levelMaker.py file
#		 in the actual game it is not used to access sprites, so it takes up
#        twice the memory than required when playing the game, if you want you 
#        can comment out its declaration and uses and un-comment them when you want
#		 to make levels to save memory, but the difference is negligible


# P.S.   The reson I didn't do it, is because I am lazy
class GraphicsLoader:

	def __init__(self):
		self.sprites_total = 0
		self.enemies = {}
		self.walls = {}
		self.player_frames = {
		"left" : [],
		"right" : [],
		"up" : [],
		"down" : []
		}
		self.coins = []

		# up, down, right, left represent the sprite types which represent those animations for enemies
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
		self.load_coin_frames()

	# loads the png frames of each wall type from the graphics folder in current working directory
	def load_wall_images(self):
		image = pg.image.load("graphics/walls.png").convert_alpha()
		for i in range(image.get_width() // WALL_WIDTH):
			for j in range(image.get_height() // WALL_HEGIHT):
				temp = pg.Surface((WALL_WIDTH, WALL_HEGIHT))
				temp.blit(image, (0, 0), (i * WALL_WIDTH, j * WALL_HEGIHT, WALL_WIDTH, WALL_HEGIHT))
				temp.set_colorkey((0, 0, 0))
				temp = pg.transform.scale(temp, (WALL_MAP_WIDTH, WALL_MAP_HEIGHT))
				self.sprites[self.sprites_total] = {"wall" + str(self.sprites_total + 1) : temp}
				self.walls["wall" + str(self.sprites_total + 1)] = temp
				self.sprites_total += 1

	def load_player_images(self):
		image = pg.image.load("graphics/player.png").convert_alpha()
		count = 0
		count_map = {
		0 : "right",
		1 : "left"
		}
		for i in range(image.get_height() // PLAYER_HEIGHT):
			frames = []
			for j in range(image.get_width() // PLAYER_WIDTH):
				temp = pg.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
				temp.blit(image, (0, 0), (j * PLAYER_WIDTH, i * PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT))
				temp = pg.transform.scale(temp, (PLAYER_MAP_WIDTH, PLAYER_MAP_HEIGHT))
				temp.set_colorkey((0, 0, 0))
				self.sprites[self.sprites_total] = {"player" + str(i) : temp}
				frames.append(temp)
				self.sprites_total += 1
			self.player_frames[count_map[count]] = frames
			count += 1

		# making the upwards player frames
		temp = []
		for frame in self.player_frames["right"]:
			frame = pg.transform.rotate(frame, 90)
			temp.append(frame)
		self.player_frames["up"] = temp

		temp = []
		# making the down player frames
		for frame in self.player_frames["right"]:
			frame = pg.transform.rotate(frame, -90)
			temp.append(frame)
		self.player_frames["down"] = temp

	def load_coin_frames(self):
		image = pg.image.load("graphics/coin.png").convert_alpha()
		for i in range(image.get_width() // COIN_WIDTH):
			for j in range(image.get_height() // COIN_HEIGHT):
				temp = pg.Surface((COIN_WIDTH, COIN_HEIGHT))
				temp.blit(image, (0, 0), (i * COIN_WIDTH, j * COIN_HEIGHT, COIN_WIDTH, COIN_HEIGHT))
				temp = pg.transform.scale(temp, (COIN_MAP_WIDTH, COIN_MAP_HEIGHT))
				temp.set_colorkey((0, 0, 0))
				self.sprites[self.sprites_total] = {"coin" + str(i) : temp}
				self.coins.append(temp)
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
					temp.set_colorkey((0, 0, 0))
					temp = pg.transform.scale(temp, (ENEMY_MAP_WIDTH, ENEMY_MAP_HEIGHT))
					self.sprites[self.sprites_total] = {"enemy" + str(count) : temp}
					self.sprites_total += 1
					types.append("enemy" + str(count))
					anims.append(temp)
					count += 1
				self.enemy_anims[enemey_color_index[enemey_color_index_count]][anim_index[anim_index_count]] = anims
				anim_index_count += 1
			self.enemies[tuple(types)] = enemey_color_index[enemey_color_index_count]
			enemey_color_index_count += 1
