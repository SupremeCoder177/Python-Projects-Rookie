# image utility

import pygame as pg
import os

'''Custom exception class for when a path given as argument does not exsist'''
class NoSuchPath(Exception):
	def __init__(self, *args, **kwargs):
		pass

'''Custom exception class for when a string argument which is expected to be a file extension name, does not match valid requirements'''
class InvalidExtensionName(Exception):
	def __init__(self, *args, **kwargs):
		pass


def dictionarize_imgs(path : str, ext : str) -> dict[str : pg.image.load]:
	'''Returns a dictionary of all images of specified extensions
	   with the image name being the keys and the image objects 
	   being the values corresponding to the name
	'''
	if not os.path.exists(path):
		raise  NoSuchPath(f"The path given {path}, does not exist in current file system")
	if not ext.startswith('.'):
		raise InvalidExtensionName(f"The given extension name {ext} is not valid. Perhaps you're missing a '.'?")

	output = {}

	for file in os.listdir(path):
		if os.path.isfile(os.path.join(path, file)):
			if file.endswith(ext):
				output[file[:len(file) - len(ext)]] = pg.image.load(f'{path}/{file}')

	return output