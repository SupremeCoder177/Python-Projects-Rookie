# this program is kind of a complementary program
# to my Specialized Platformer Level Maker
# I mean the whole point of making pixel levels is to turn
# them into levels to play

import pygame as pg
import os
from json import load


# tries to load a level from a file path, and well doesn't load the data unless 
# the data is in the appropriate format
class PixelLevelLoader:

	def __init__(self, file_path, convert):
		if not os.path.exists(file_path):
			print("Bro this aint a valid path to a file !!") # could I have done something better than this? Probably yes
			return
		if not os.path.isfile(file_path):
			print("This isn't a file !")
			return
		self.tile_positions = dict()
		self.images = dict()
		with open(file_path, 'r') as f:
			temp = load(f)
			self.load_tile_pos(temp)
			self.load_tile_images(temp, convert, os.path.split(file_path)[0])

	# calculates the tile positions and puts them
	# in a dict, if you want to keep the stacking order
	# then only render the tiles from index 0
	def load_tile_pos(self, data):
		for tiles in data.values():
			for tile in tiles.values():
				try:
					self.tile_positions[tuple(tile["pos"])] = tile["img_path"]
				except KeyError as e:
					# stop reading the data
					return

	# loads all the images used in the level and puts them in
	# a dict called self.images
	def load_tile_images(self, data, convert, path):
		temp = os.getcwd()
		os.chdir(path)
		for tiles in data.values():
			for tile in tiles.values():
				try:
					if tile["img_path"] not in self.images:
						self.images[tile["img_path"]] = pg.image.load(tile["img_path"]).convert_alpha() if convert else pg.image.load(tile["img_path"])
				except KeyError as e:
					# stop reading the data
					os.chdir(temp)
					return

	# returns the dict of the loaded images
	def get_images(self):
		return self.images

	# returns the positions dict
	def get_positions(self):
		return self.tile_positions