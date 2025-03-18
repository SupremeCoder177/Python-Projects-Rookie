# Entity file to hold all game entities

import pygame as pg
import math

'''Basic Entity Class Which will be the parent class for all customized game entities
	
	This class keeps track of the surface the entity renders on, the image it uses and 
	the movement speed and direction, also this class uses absolute screen coordinates instead of
	grid coordinates

'''
class Entity:	

	def __init__(self, surf : pg.Surface, img : pg.Surface, speed : float, direction : float, coords : list[float]):
		self.surf = surf
		self.img = img
		self.orignal_img = img
		self.speed = speed
		self.direction = direction
		self.coor = coords

		self.img = pg.transform.rotate(self.img, self.direction)

	# renders the entity on the given surface
	def render(self):
		rect = self.img.get_rect(topleft = self.coor)
		self.surf.blit(self.img, rect)

	# move the entity in the direction with the speed as the step value
	# but since we may want to decide the step value to be different 
	# for some cases hence the argument is provided for it
	def move(self, step=None) -> None:
		if not step: step = self.speed
		dx = -math.cos(math.radians(self.direction)) * step
		dy = -math.sin(math.radians(self.direction)) * step
		self.coor[0] += dx
		self.coor[1] += dy

	# changes the direction and rotates the image too
	# also the rotation is in the counter-clockwise direction
	def rotate(self, angle : float) -> None:
		temp = self.orignal_img.copy()
		self.direction -= angle
		self.img = pg.transform.rotate(temp, self.direction)

	# shows the direction of the entity movement as a line drawn on the render surface
	def show_direction(self, color, steps) -> None:
		dx = self.orignal_img.get_width() // 2 + (self.coor[0] + math.cos(math.radians(self.direction)) * steps)
		dy = self.coor[1] + (math.sin(math.radians(self.direction))) * steps

		pg.draw.line(self.surf, color, (self.orignal_img.get_width() // 2 + self.coor[0], self.coor[1]), (dx, dy))



class Player(Entity):

	def __init__(self, surf : pg.Surface, img : pg.Surface, speed : float, direction : float, coors : list[float]):
		super().__init__(surf = surf, img = img, speed = speed, direction = direction, coords = coors)





