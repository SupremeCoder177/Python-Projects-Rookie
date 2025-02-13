# a controller for controlling the falling brick

import pygame as pg
from time import time

'''This class will handle all the user
   input and update the falling brick accordingly
'''
class Controller:

	def __init__(self, renderer) -> None:
		self.renderer = renderer
		self.data = renderer.data
		self.btns = {
			pg.K_UP : False,
			pg.K_DOWN : False,
			pg.K_LEFT : False,
			pg.K_RIGHT : False
		}
		self.last_move_time = 0
		self.last_rotate_time = 0
		self.move_cooldown = 0.05
		self.rotate_cooldown = 0.1

	'''Changes the pressed status of the
	   key that was pressed, that is if the
	   key is in the btns dictionary
	'''
	def press(self, event):
		if event in self.btns:
			self.btns[event] = True

	'''Opposite function of press function'''
	def lift(self, event):
		if event in self.btns:
			self.btns[event] = False

	'''Updating the falling brick according to
	   the buttons that are pressed
	'''
	def update(self):
		if not self.renderer.get_falling_brick(): return

		current_time = time()
		temp = self.renderer.get_falling_brick().get_coor()

		if current_time - self.last_move_time > self.move_cooldown:
			if self.btns[pg.K_LEFT]:
				temp[0] -= self.data["brick_move_speed"]
			if self.btns[pg.K_RIGHT]:
				temp[0] += self.data["brick_move_speed"]
			self.last_move_time = current_time

		if current_time - self.last_rotate_time > self.rotate_cooldown:
			if self.btns[pg.K_UP]:
				curr_index = self.renderer.get_falling_brick().get_orient()
				curr_index = (curr_index + 1) % self.renderer.get_falling_brick().get_orients()
				self.renderer.get_falling_brick().set_orient_index(curr_index)
			self.last_rotate_time = current_time

		if self.btns[pg.K_DOWN]:
			self.renderer.set_fall_fast()

