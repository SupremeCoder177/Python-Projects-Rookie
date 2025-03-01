# Brick Class and Factory

from random import choice, randint
import pygame as pg


class BrickFactory:

	type_1 = {
			0 : lambda x, y, tile_size: ((x, y), (x, y + tile_size), (x + tile_size, y), (x + tile_size, y + tile_size))
		}


		# the  0    000    0      0  brick types
		#     000    0     00    00
		#                  0      0
	type_2 = {
			2 : lambda x, y, tile_size: ((x, y), (x + tile_size, y), (x - tile_size, y), (x, y - tile_size)),
			3 : lambda x, y, tile_size: ((x, y), (x + tile_size, y), (x, y + tile_size), (x, y - tile_size)),
			1 : lambda x, y, tile_size: ((x, y), (x - tile_size, y), (x, y + tile_size), (x, y - tile_size)),
			0 : lambda x, y, tile_size: ((x, y), (x + tile_size, y), (x - tile_size, y), (x, y + tile_size))
		}

		# the 0000 and 0 brick type
		#			   0
		#			   0
		#			   0
	type_3 = {	
			0 : lambda x, y, tile_size: ((x, y), (x, y - tile_size), (x, y + tile_size), (x, y + (tile_size * 2))),
			1 : lambda x, y, tile_size : ((x, y), (x + tile_size, y), (x - tile_size, y), (x + (tile_size * 2), y))
		}

		# the    00   00   brick types
		#		00     00

	type_4 = {
			0 : lambda x, y, tile_size: ((x, y), (x + tile_size, y), (x, y + tile_size), (x - tile_size, y + tile_size)),
			1 : lambda x, y, tile_size: ((x, y), (x, y - tile_size), (x + tile_size, y), (x + tile_size, y + tile_size))
		}
	type_5 = {
			0 : lambda x, y, tile_size: ((x, y), (x - tile_size, y), (x, y + tile_size), (x + tile_size, y + tile_size)),
			1 : lambda x, y, tile_size: ((x, y), (x, y - tile_size), (x - tile_size, y), (x - tile_size, y + tile_size))
		}

	type_6 = {
		0 : lambda x, y, tile_size: ((x, y), (x + tile_size, y), (x, y - tile_size), (x, y - (2 * tile_size))),
		1 : lambda x, y, tile_size: ((x, y), (x, y + tile_size), (x + tile_size, y), (x + (2 * tile_size), y)),
		2 : lambda x, y, tile_size: ((x, y), (x - tile_size, y), (x, y + tile_size), (x, y + (2 * tile_size))),
		3 : lambda x, y, tile_size: ((x, y), (x, y - tile_size), (x - tile_size, y), (x - (2 * tile_size), y))
	}

	imgs = {
	"red" : pg.image.load("Images/red.png"),
	"blue" : pg.image.load("Images/blue.png"),
	"green" : pg.image.load("Images/green.png"),
	"orange" : pg.image.load("Images/orange.png"),
	"yellow" : pg.image.load("Images/yellow.png"),
	"white" : pg.image.load("Images/white.png")
	}

	types = [type_1, type_2, type_3, type_4, type_5, type_6]

	@classmethod
	def get_brick(cls):
		return choice(cls.types), choice(list(cls.imgs.items()))


class Brick:

	def __init__(self, surface, brick, coor, index, tile_size):
		self.surf = surface
		self.func = brick[0]
		self.color = brick[1][0]
		self.img = brick[1][1]
		self.coor = coor
		self.index = index
		self.tile_size = tile_size

	def render(self):
		for tile in self.get_tiles():
			self.surf.blit(self.img, tile)

	def get_tiles(self):
		return [tile for tile in self.func[self.index](self.coor[0] * self.tile_size, self.coor[1] * self.tile_size, self.tile_size)]

	def inc_index(self):
		self.index += 1
		if self.index >= len(self.func):
			self.index = 0

	def dec_index(self):
		self.index -= 1
		if self.index < 0:
			self.index = len(self.func) - 1

	def move_down(self, inc):
		self.coor[1] += inc

	def move_up(self, dec):
		self.coor[1] -= dec

	def move_left(self, dec):
		self.coor[0] -= dec

	def move_right(self, inc):
		self.coor[0]  += inc


class BricksManager:

	def __init__(self, game, surf, data):
		self.surf = surf
		self.game = game
		self.data = data
		self.curr_brick = None
		self.occupied = {}

	def add_brick(self):
		if self.curr_brick:
			for tile in self.curr_brick.get_tiles():
				self.occupied[tile] = self.curr_brick.img

		temp = BrickFactory.get_brick()
		index = randint(0, len(temp[0]) - 1)
		width = self.data["grid_size"][0] // self.data["tile_size"]
		coor = [width // 2, 0]
		self.curr_brick = Brick(self.surf, temp, coor, index, self.data["tile_size"])

	def render(self):
		if not self.curr_brick: return
		self.curr_brick.render()

		for tile in self.occupied:
			self.surf.blit(self.occupied[tile], tile)

	def apply_gravity(self):
		self.curr_brick.move_down(1)

	def check_floor_contact(self):
		if self.check_offset(self.curr_brick):
			self.curr_brick.move_up(1)
			self.add_brick()
			self.game.reset_timer()
			self.game.score += 100

	def check_brick_contact(self):
		if self.check_brick_offset(self.curr_brick):
			self.curr_brick.move_up(1)
			self.add_brick()
			self.game.reset_timer()
			self.game.score += 100

	def update(self):
		if not self.curr_brick: self.add_brick()
		self.apply_gravity()
		self.check_collision()

	def check_collision(self):
		self.check_floor_contact()
		self.check_brick_contact()

	def check_offset(self, brick):
		for tile in brick.get_tiles():
			if not 0 + self.data["grid_x_offset"] <= tile[0]: return True
			if not self.data["grid_size"][0] + self.data["grid_x_offset"] >= tile[0] + self.data["tile_size"]: return True
			if not 0 + self.data["grid_y_offset"] <= tile[1]: return True
			if not self.data["grid_size"][1] + self.data["grid_y_offset"] >= tile[1] + self.data["tile_size"]: return True
		return False

	def check_brick_offset(self, brick):
		for tile in brick.get_tiles():
			if tile in self.occupied: return True
		return False

	def move(self, degree):
		if degree > 0:
			self.curr_brick.move_right(self.data["brick_move_speed"])
		else:
			self.curr_brick.move_left(self.data["brick_move_speed"])

		if self.check_offset(self.curr_brick) or self.check_brick_offset(self.curr_brick):
			if degree > 0:
				self.curr_brick.move_left(self.data["brick_move_speed"])
			else:
				self.curr_brick.move_right(self.data["brick_move_speed"])

	def change_index(self, degree):
		if degree > 0:
			self.curr_brick.inc_index()
		else:
			self.curr_brick.dec_index()

		if self.check_offset(self.curr_brick) or self.check_brick_offset(self.curr_brick):
			if degree > 0:
				self.curr_brick.dec_index()
			else:
				self.curr_brick.inc_index()

	def get_occupied(self):
		return list(self.occupied.keys())

	def move_down_occupied(self, row):
		deletion = []
		move_down = []
		for tile in self.occupied:
			if tile[1] // self.data["tile_size"] < row: move_down.append(tile)
			if tile[1] // self.data["tile_size"] == row: deletion.append(tile)

		for tile in deletion:
			del self.occupied[tile]

		for tile in move_down:
			img = self.occupied[tile]
			del self.occupied[tile]
			new_tile = (tile[0], tile[1] + self.data["tile_size"])
			self.occupied[new_tile] = img
		self.game.score += 1000

	def delete_all(self):
		self.curr_brick = None
		self.occupied = {}


