# brick object

'''A class which keeps track of a single brick attributes and is 
   is responsible for handling collisions and gravity
'''
class Brick:

	def __init__(self, function_dict : dict, img, orient_index=0, falling=True) -> None:
		self.falling = falling
		self.func_dict = function_dict
		self.img = index
		self.orient_index = orient_index
