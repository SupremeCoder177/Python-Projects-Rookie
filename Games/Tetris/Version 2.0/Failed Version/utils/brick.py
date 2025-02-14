# brick object

'''A class which keeps track of a single brick attributes and is 
   is responsible for handling collisions
'''
class Brick:

	def __init__(self, function_dict : dict, img : str, coor : list, tile_size : int, orient_index=0, falling=True) -> None:
		self.falling = falling
		self.func_dict = function_dict
		self.img = img
		self.orient_index = orient_index
		self.coor = coor
		self.tile_size = tile_size

	'''checks if the brick has collided with the provided brick horizontally
	   the brick in the argument should be an object of the
	   fallen brick class
	'''
	def collide_horizontal(self, brick) -> str:
		for coor in self.get_bricks():
			points = ((coor[0], coor[1]), (coor[0] + self.tile_size, coor[1]))
			for point in points:
				if brick.y <= point[1] <= brick.y + self.tile_size:
					if brick.x <= point[0] <= brick.x + self.tile_size:
						if points.index(point) == 0: return "left"
						else: return "right"
		return None

	'''Checks if the brick has colided with another brick on the floor, vertically
		aka only checks if the bottom of all the sub-bricks of the falling brick
		if in contact with any other fallen brick
	'''
	def collide_vertical(self, brick) -> bool:
		count = 0
		for coor in self.get_bricks():
			points = ((coor[0], coor[1] + self.tile_size), (coor[0] + self.tile_size, coor[1] + self.tile_size))
			for point in points:
				if brick.x <= point[0] <= brick.x + self.tile_size:
					if brick.y <= point[1] <= brick.y + self.tile_size:
						count += 1
		return True if count > 2 else False

	def align_vertical(self, brick) -> None:
		lowest = self.get_bricks()[0][1]
		for coor in self.get_bricks():
			if coor[1] < lowest: lowest = coor[1]

	'''Align the brick with given coors'''
	def align_with(self, x, y) -> None:
		self.coor[0] = x // self.tile_size
		self.coor[1] = y // self.tile_size

	'''Returns the coordinates of all the sub-bricks'''
	def get_bricks(self) -> None:
		return [coor for coor in self.func_dict[self.orient_index](self.coor[0] * self.tile_size, self.coor[1] * self.tile_size, self.tile_size)]

	'''Aligns brick horizontally with left or right side of another fallend brick'''
	def align_horizontal(self, brick, side) -> None:
		pass

	'''Turns off the falling variable'''
	def stop_falling(self) -> None:
		self.falling = False

	'''Returns the no of orientations the brick has'''
	def get_orients(self) -> int:
		return len(self.func_dict)

	'''Returns the brick's main coor'''
	def get_coor(self) -> list:
		return self.coor

	'''Returns the orient index'''
	def get_orient(self) -> int:
		return self.orient_index

	'''Sets orient index to given index'''
	def set_orient_index(self, index) -> None:
		if 0 <= index < len(self.func_dict):
			self.orient_index = index

'''A class which represents individual bricks
	which lie on the floor and do not move
'''
class FallenBrick:
	'''This class only keeps track of the brick's position and 
		the image that is used to display it
	'''
	def __init__(self, x : int, y : int, img) -> None:
		self.x = x
		self.y = y
		self.img = img

