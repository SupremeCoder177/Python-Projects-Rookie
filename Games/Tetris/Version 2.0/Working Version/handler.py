# Input Handler

import pygame as pg

class Handler:

	def __init__(self, game, manager):
		self.manager = manager
		self.game = game
		self.input_map = {
			(pg.K_w, pg.K_UP) : lambda : self.manager.change_index(1),
			(pg.K_s, pg.K_DOWN) : self.change_timer,
			(pg.K_a, pg.K_LEFT) : lambda: self.manager.move(-1),
			(pg.K_d, pg.K_RIGHT) : lambda: self.manager.move(1)
		}
		self.input_state = {
		pg.K_w : False,
		pg.K_a : False,
		pg.K_s : False,
		pg.K_d : False,
		pg.K_UP : False,
		pg.K_DOWN : False,
		pg.K_RIGHT : False,
		pg.K_LEFT : False
		}

	def change_timer(self):
		self.game.timer = 1 / self.game.data["brick_inc_fall_speed"]

	def change_input_state(self, event):
		if event.type == pg.KEYDOWN:
			if event.key in self.input_state:
				self.input_state[event.key] = True

		if event.type == pg.KEYUP:
			if event.key in self.input_state:
				self.input_state[event.key] = False

	def handle(self):
		for key in self.input_state:
			if self.input_state[key]:
				for types in self.input_map:
					if key in types:
						self.input_map[types]()
