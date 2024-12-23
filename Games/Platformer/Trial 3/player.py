# Player

from collision import *

class Player:

	def __init__(self, screen, map_, color, width, height):
		self.screen = screen
		self.color = color
		self.map = map_
		self.player_rect = pg.Rect(self.map.get_player_pos()[0] * COL_SIZE, self.map.get_player_pos()[1] * COL_SIZE, width, height)
		self.velocity = 0
		self.wanna_jump = False
		self.direction_x = [0, 0]
		self.player_speed = PLAYER_SPEED

	def update(self, fall: bool) -> None:
		self.direction_x = [0, 0]
		self.check_collision()
		if fall: 
			self.inc_velocity()
		self.apply_gravity()
		self.get_input()
		self.draw()

	def inc_velocity(self):
		self.velocity = min(PLAYER_MAX_ACC, self.velocity + PLAYER_ACC)

	def get_input(self):
		keys = pg.key.get_pressed()
		if keys[pg.K_SPACE]:
			self.velocity = - PLAYER_JUMP_VAL
			self.wanna_jump = True
			self.fall = True
		if keys[pg.K_LEFT]:
			self.player_rect.x -= self.player_speed
			self.direction_x = [1, 0]
		if keys[pg.K_RIGHT]:
			self.player_rect.x += self.player_speed
			self.direction_x = [0, 1]

	def check_collision(self):
		collide_tiles = Collision(self.screen, self, self.map).get_collide_tiles()
		# print(collide_tiles.get('left', None))
		if collide_tiles.get('vertical_down', None) and not self.wanna_jump:
			self.fall = False
			self.velocity = 0
			self.player_rect.bottom = collide_tiles['vertical_down'].top
		if collide_tiles.get('vertical_up', None):
			self.fall = True
			self.player_rect.top = collide_tiles['vertical_up'].bottom
		if collide_tiles.get('left', None):
			self.player_speed = 0
			self.player_rect.left = collide_tiles['left'].right
		if collide_tiles.get('right', None):
			self.player_speed = 0
			self.player_rect.right = collide_tiles['right'].left

	def apply_gravity(self):
		self.player_rect.y += self.velocity

	def draw(self):
		pg.draw.rect(self.screen, self.color, self.player_rect)

	def get_pos(self):
		return [int(self.player_rect.x // COL_SIZE), int(self.player_rect.y // COL_SIZE)]

