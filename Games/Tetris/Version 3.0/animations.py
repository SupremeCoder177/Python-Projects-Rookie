# this module handles the animation logic

import pygame as pg
import os


# loads a single image (if exists)
def load_image(fp):
	if not os.path.exists(fp) or not os.path.isfile(fp):
		return None
	return pg.image.load(fp).convert_alpha()


# loads all images in the directory with a specific extensions set (if exists)
def load_images(fp):
	if not os.path.exists(fp): return 

	extensions = [".png", ".jpeg", ".jpg"]
	out = []
	for file in os.listdir(fp):
		for ext in extensions:
			if file.endswith(ext):
				out.append(load_image(os.path.join(fp, file)))
	return out


# this class represents a single animation sequence of a tileset
# this class supports only horizontal tilesets
class Animation:

	def __init__(self, fp : str, tile_size : int, frames : int):
		self.num_images = 0
		self.image = None
		self.tile_size = tile_size
		self.frames = frames
		self.img_index = 0
		self.calc_images(fp)

	# loads all sprites in the tilesheet
	def calc_images(self, fp : str):
		self.image = load_image(fp)
		if not self.image: return
		self.num_images = self.image.get_width() // self.tile_size

	# change the current sprite images if a certain number of frames has elapsed
	# remember all animations must be updated with each iteration of the game loop
	# or the animation will not work as expected
	def update(self, frames_elapsed : int):
		if not frames_elapsed % self.frames:
			self.img_index += 1
			self.img_index %= self.num_images

	# draws the animation on a given surface and coordinates
	def draw(self, x : int, y : int, surface : pg.Surface, tile_size: int):
		rect = pg.Rect((x, y, tile_size, tile_size))
		surface.blit(pg.transform.scale(self.image.subsurface((self.img_index * self.tile_size, 0, self.tile_size, self.tile_size)), (tile_size, tile_size)), rect)

	# when starting the animation remember to reset it
	def reset(self):
		self.img_index = 0