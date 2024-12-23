# player for platformer trial 2

from map import *


class Player:

	def __init__(self, screen, pos, ply_width, ply_height, color):
		self.screen = screen
		self.player = pg.Rect(pos[0] * COL_SIZE, pos[1] * COL_SIZE, ply_width, ply_height)
		self.color = color
		self.velocity = 0
		self.direction_x = [0, 0]
		self.direction_y = [0, 1]
		self.player_speed = PLAYER_SPEED
		self.stop_velocity = False
		self.input = True

	def update(self):
		self.direction_x = [0, 0]
		self.apply_gravity()
		if self.input: self.get_input()
		self.draw()

	def draw(self):
		pg.draw.rect(self.screen, self.color, self.player)

	def apply_gravity(self):
		self.velocity = min(10, self.velocity + PLAYER_ACC)
		if self.stop_velocity: self.velocity = 0
		self.player.bottom += self.velocity
		if self.velocity > 0: 
			self.direction_y = [0, 1]

	def get_input(self):
		keys = pg.key.get_pressed()
		if keys[pg.K_LEFT]:
			self.player.x -= self.player_speed
			self.direction_x = [1, 0]
		if keys[pg.K_RIGHT]:
			self.player.x += self.player_speed
			self.direction_x = [0, 1]
		if keys[pg.K_SPACE]:
			self.velocity = - PLAYER_JUMP_VAL
			self.stop_velocity = False
			self.direction_y = [1, 0]

	def get_pos(self):
		return [int(self.player.x // COL_SIZE), int(self.player.y // COL_SIZE)]

