# this module handles the bricks (all about bricks LOL)

import pygame as pg
from animations import Animation
from typing import List
from random import choice, randint

# this class generates brick types, colors and animations
class BrickFactory:

	""" 
		the 
	  	##
	 	 ##  brick type
	"""
	brick1 = {
		0 : lambda x, y, ts: ((x, y), (x + ts, y), (x, y + ts), (x + ts, y + ts))
	}

	""" the
	  	#
	  	### brick type
	 """
	brick2 = {
	 0 : lambda x, y, ts: ((x, y), (x, y - ts), (x + ts, y), (x + 2 * ts, y)),
	 1 : lambda x, y, ts: ((x, y), (x + ts, y), (x, y + ts), (x, y + 2 * ts)),
	 2 : lambda x, y, ts: ((x, y), (x - ts, y), (x - 2 * ts, y), (x, y + ts)),
	 3 : lambda x, y, ts: ((x, y), (x - ts, y), (x, y - ts), (x, y - 2 * ts))
	}

	""" 
		the
	      #
		### brick type
	"""
	brick3 = {
	 0 : lambda x, y, ts: ((x, y), (x - ts, y), (x - 2 * ts, y), (x, y - ts)),
	 1 : lambda x, y, ts: ((x, y), (x + ts, y), (x, y - ts), (x, y - 2 * ts)),
	 2 : lambda x, y, ts: ((x, y), (x, y + ts), (x + ts, y), (x + 2 * ts, y)),
	 3 : lambda x, y, ts: ((x, y), (x - ts, y), (x, y + ts), (x, y + 2 * ts))
	}

	"""
		the
		 #
		### brick type
	"""
	brick4 = {
	 0 : lambda x, y, ts: ((x, y), (x - ts, y), (x + ts, y), (x, y - ts)),
	 1 : lambda x, y, ts: ((x, y), (x + ts, y), (x, y - ts), (x, y + ts)),
	 2 : lambda x, y, ts: ((x, y), (x - ts, y), (x + ts, y), (x, y + ts)),
	 3 : lambda x, y, ts: ((x, y), (x - ts, y), (x, y - ts), (x, y + ts))
	}

	"""
		the
		#### brick type
	"""	
	brick5 = {
	 0 : lambda x, y, ts: ((x, y), (x - ts, y), (x + ts, y), (x + 2 * ts, y)),
	 1 : lambda x, y, ts: ((x, y), (x, y - ts), (x, y + ts), (x, y + 2 * ts))
	}

	"""
		the
  		 ##
		## brick type
	"""

	brick6 = {
	 0 : lambda x, y, ts : ((x, y), (x - ts, y), (x, y - ts), (x + ts, y - ts)),
	 1 : lambda x, y, ts : ((x, y), (x + ts, y), (x, y - ts), (x + ts, y + ts))
	}

	"""
		the
		##
		 ## brick type
	"""

	brick7 = {
	 0 : lambda x, y, ts: ((x, y), (x, y - ts), (x - ts, y - ts), (x + ts, y)),
	 1 : lambda x, y, ts: ((x, y), (x + ts, y), (x + ts, y - ts), (x, y + ts))
	}

	bricks = [brick1, brick2, brick3, brick4, brick5, brick6, brick7]
	colors = ["blue", "green", "magenta", "yellow"]

	# returns a random brick type
	def get_brick(self):
		return choice(self.bricks)

	# returns a random brick color
	def get_color(self):
		return choice(self.colors)

	# returns all the colors
	def get_all_colors(self):
		return self.colors

	# returns a animation based on the color given
	# change the code here for changing brick animation
	def get_animation(self, color : str):
		return Animation(f"Images/Blocks/{color.capitalize()}/{color}.png", 32, 7)


# this class defines the falling brick
class Brick:

	def __init__(self, game):
		self.game = game
		self.settings = game.settings
		self.anim = None
		self.pos = [0, 0]
		self.index = 0
		self.fall_speed = 2 # tiles per second
		self.inc_fall_speed = 3 # tiles per second
		self.new_frames_movement = self.settings["fps"] // self.inc_fall_speed
		self.frames_per_movement = self.settings["fps"] // self.fall_speed
		self.input_speed = 0.2 # every one second
		self.input_frames = int(self.settings["fps"] * self.input_speed)
		self.color = None
		self.gen_brick()

	# generate a random brick type and a random position, and the animation based on a random color
	def gen_brick(self):
		self.brick = BrickFactory().get_brick()
		while True:
			x = randint(0, self.settings["grid_size"][0] // self.settings["tile_size"])
			found = True
			for type in self.brick:
				for pos in self.brick[type](x * self.settings["tile_size"], -self.settings["tile_size"], self.settings["tile_size"]):
					if pos[0] < 0 or pos[0] + self.settings["tile_size"] > self.settings["grid_size"][0]:
						found = False
						break
				if not found: break
			if found:
				self.pos[0] = x * self.settings["tile_size"]
				break
		self.pos[1] = -self.settings["tile_size"]
		self.color = BrickFactory().get_color()
		self.anim = BrickFactory().get_animation(self.color)
		self.index = randint(0, len(self.brick) - 1)

	# draws the brick on a given surface
	def draw(self, surface : pg.Surface):
		img = self.anim.get_current_frame()
		transformed_img = pg.transform.scale(img, (self.settings["tile_size"], self.settings["tile_size"]))
		for pos in self.brick[self.index](self.pos[0], self.pos[1], self.settings["tile_size"]):
			surface.blit(transformed_img, (pos[0] + self.settings["grid_pos"][0], pos[1] + self.settings["grid_pos"][1], self.settings["tile_size"], self.settings["tile_size"]))

	# update the brick animation
	def update(self):

		# updating the animation frame
		self.anim.update(self.game.frames_elapsed)

		# updating the y position
		if not self.game.frames_elapsed % self.frames_per_movement:
			self.pos[1] += self.settings["tile_size"]
		# checking for floor contact
			if self.check_floor_collision() or self.check_brick_collision():
				self.reset()
		
		# taking input
		if not self.game.frames_elapsed % self.input_frames:
			self.take_input()

	# taking player input
	# and returns checks collision with out of bounds and with other bricks
	def take_input(self):
		keys = pg.key.get_pressed()

		delta_x = 0
		# changing the x position
		if keys[pg.K_LEFT]:
			delta_x -= self.settings["tile_size"]
		if keys[pg.K_RIGHT]:
			delta_x += self.settings["tile_size"]

		# applying movement and checking for collision
		if delta_x:
			self.pos[0] += delta_x
			if self.check_brick_collision() or self.check_out_of_bounds():
				self.pos[0] -= delta_x

		# changing the brick index and checking for collision
		old_index = self.index
		if keys[pg.K_UP]:
			self.index += 1
			self.index %= len(self.brick)

			if self.check_out_of_bounds() or self.check_brick_collision():
				self.index = old_index

		if keys[pg.K_DOWN]:
			self.frames_per_movement = self.new_frames_movement

	# checking if the brick is out of bounds
	def check_floor_collision(self) -> bool:
		for pos in self.brick[self.index](self.pos[0], self.pos[1], self.settings["tile_size"]):
			if pos[1] >= self.settings["grid_size"][1]: return True
		return False

	# checking for out of bounds
	def check_out_of_bounds(self) -> bool:
		for pos in self.brick[self.index](self.pos[0], self.pos[1], self.settings["tile_size"]):
			if pos[0] < 0 or pos[0] + self.settings["tile_size"] > self.settings["grid_size"][0]: return True
			if pos[1] + self.settings["tile_size"] > self.settings["grid_size"][1]: return True
		return False

	# checking brick collision and out of bounds collision
	def check_brick_collision(self) -> bool:
		occupied = tuple(self.game.coor_map.keys())
		for pos in self.brick[self.index](self.pos[0], self.pos[1], self.settings["tile_size"]):
			for tile in occupied:
				if pos == tile:
					return True
		return False

	# reseting the brick
	def reset(self):
		self.pos[1] -= self.settings["tile_size"]
		self.frames_per_movement = self.settings["fps"] // self.fall_speed
		self.game.add_brick(self.brick[self.index](self.pos[0], self.pos[1], self.settings["tile_size"]), self.color)
		self.gen_brick()
