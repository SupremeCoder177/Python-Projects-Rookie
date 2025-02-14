# brick factory for tetris

from random import randint

class BrickFactory:
	'''Brick factory to store various brick types
	   in form of index mapped lambda functions, for each
	   index representing an orientation of the brick
	'''
	def __init__(self):

		# the   00  brick type
		#       00
		self.type_1 = {
			0 : lambda x, y, tile_size: ((x, y), (x, y + tile_size), (x + tile_size, y), (x + tile_size, y + tile_size))
		}


		# the  0    000    0      0  brick types
		#     000    0     00    00
		#                  0      0
		self.type_2 = {
			0 : lambda x, y, tile_size: ((x, y), (x + tile_size, y), (x - tile_size, y), (x, y - tile_size)),
			1 : lambda x, y, tile_size: ((x, y), (x + tile_size, y), (x, y + tile_size), (x, y - tile_size)),
			2 : lambda x, y, tile_size: ((x, y), (x - tile_size, y), (x, y + tile_size), (x, y - tile_size)),
			3 : lambda x, y, tile_size: ((x, y), (x + tile_size, y), (x - tile_size, y), (x, y + tile_size))
		}

		# the 0000 and 0 brick type
		#			   0
		#			   0
		#			   0
		self.type_3 = {	
			0 : lambda x, y, tile_size: ((x, y), (x, y - tile_size), (x, y + tile_size), (x, y + (tile_size * 2))),
			1 : lambda x, y, tile_size : ((x, y), (x + tile_size, y), (x - tile_size, y), (x + (tile_size * 2), y))
		}

		# the    00   00   brick types
		#		00     00

		self.type_4 = {
			0 : lambda x, y, tile_size: ((x, y), (x + tile_size, y), (x, y + tile_size), (x - tile_size, y + tile_size)),
			1 : lambda x, y, tile_size: ((x, y), (x, y - tile_size), (x + tile_size, y), (x + tile_size, y + tile_size))
		}
		self.type_5 = {
			0 : lambda x, y, tile_size: ((x, y), (x - tile_size, y), (x, y + tile_size), (x + tile_size, y + tile_size)),
			1 : lambda x, y, tile_size: ((x, y), (x, y - tile_size), (x - tile_size, y), (x - tile_size, y + tile_size))
		}

		self.types = [self.type_1, self.type_2, self.type_3, self.type_4, self.type_5]

	# function to get a random brick funtion
	def get_brick(self, type : int) -> dict:
		return self.types[type]

	# function to return the no of brick types
	def type_size(self) -> int:
		return len(self.types)