# Player 

import pygame as pg

class Player:

	def __init__(self, game):
		self.width = 25
		self.height = 40
		self.clr = "red"
		self.game = game
		self.gravity = game.settings["gravity"]
		self.pos = [game.settings["player_pos"][0] * game.settings["tile_size"], game.settings["player_pos"][1] * game.settings["tile_size"]]
		self.jump_count = 2
		self.jump_key_released = True
		self.x_collide = self.y_collide = 0
		self.last_horizontal_collide = 0

	def draw(self):
		tile_size = self.game.settings["tile_size"]
		pg.draw.rect(self.game.screen, self.clr, (self.pos[0] + self.game.offset_x, self.pos[1] + self.game.offset_y, self.width, self.height))

	def apply_gravity(self):
		collide = self.check_collision_vertical(self.gravity)
		if collide:
			if self.gravity <= 0:
				self.y_collide = -1
				self.gravity = self.game.settings["gravity"]
			else:
				self.y_collide = 1
		else:
			self.y_collide = 0
		self.gravity = min(self.gravity + self.game.settings["gravity_acc"], self.game.settings["max_gravity"]) if self.y_collide == 0 else self.gravity
		
		# resetting jump count
		if self.y_collide > 0:
			self.jump_count = 2

		# attaching player bottom to the bottom tile
		if self.y_collide > 0:
			while not self.check_collision_vertical(1):
				pass

	def update(self):
		self.apply_gravity()
		self.take_input_continous()
		self.take_input_singles()
		self.check_slide()
		print(self.x_collide, self.y_collide)

	def take_input_continous(self):
		keys = pg.key.get_pressed()

		move_map = {
		 (pg.K_a, pg.K_LEFT) : -self.game.settings["player_move_speed"],
		 (pg.K_d, pg.K_RIGHT) : self.game.settings["player_move_speed"]
		}
		temp = 0
		# horizontal movement
		for mag, item in move_map.items():
			for key in mag:
				if keys[key]:
					if self.check_collision_horizontal(item):
						if item > 0: 
							self.x_collide = 1
						else: self.x_collide = -1
					else:
						self.x_collide = 0

	def check_slide(self):
		if self.jump_count < 1 and self.x_collide != self.last_horizontal_collide:
			self.jump_count += 1
			self.last_horizontal_collide = self.x_collide

	def take_input_singles(self):
		events = self.game.keys_held

		# jumping
		if self.jump_count > 0:
			if pg.K_SPACE in events and self.jump_key_released:
				self.gravity = self.game.settings["player_jump"]
				self.jump_key_released = False
				self.jump_count -= 1
				
		if pg.K_SPACE in self.game.released:
			self.jump_key_released = True

	def pos(self):
		return self.pos
	
	def world_pos(self):
		return int(self.pos[0] / self.game.settings["tile_size"]), int(self.pos[1] / self.game.settings["tile_size"])

	def is_blocked(self, x, y):
		tile_size = self.game.settings["tile_size"]
		return [x // tile_size, y // tile_size] in self.game.settings["world_map"]

	def check_collision_vertical(self, dy):
		x1, y1 = self.pos[0] , self.pos[1] + dy 
		x2 = x1 + self.width
		y2 = y1 + self.height
		is_blocked = self.is_blocked
		if not is_blocked(x1, y1) and not is_blocked(x2, y1) and not is_blocked(x1, y2) and not is_blocked(x2, y2):
			self.pos[1] += dy
			return False
		else:
			return True

	def check_collision_horizontal(self, dx):
		x1, y1 = self.pos[0] + dx, self.pos[1]
		x2 = x1 + self.width
		y2 = y1 + self.height
		is_blocked = self.is_blocked
		if not is_blocked(x1, y1) and not is_blocked(x2, y1) and not is_blocked(x1, y2) and not is_blocked(x2, y2) and not self.is_blocked(x1, y1 + (self.height / 2)) and not self.is_blocked(x2, y1 + (self.height / 2)):
			self.pos[0] += dx
			return False
		else:
			return True