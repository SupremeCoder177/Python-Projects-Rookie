# collison engine for tetris game

'''This class will handle the brick collisions and alignment accordingly'''
class Collider:

	def __init__(self, renderer, data):
		self.renderer = renderer
		self.data = data

	'''Checks vertical collision between falling brick and floor,
	   and also other bricks on the floor
	'''
	def check_vertical_collision(self) -> None:
		falling_brick = self.renderer.get_falling_brick()
		bricks = self.renderer.get_landed_bricks()
		main_coor = self.renderer.get_falling_brick().get_coor()

		# checking floor contact
		for coor in falling_brick.get_bricks():
			if coor[1] + self.data["tile_size"] >= self.data["game_size"][1] + self.data["game_grid_start_y"]:
				# stopping falling is collided with ground
				self.renderer.get_falling_brick().stop_falling()

				# aligning the bottom of the brick with the ground
				self.renderer.get_falling_brick().align_with(main_coor[0] * self.data["tile_size"], round(coor[1]) - (round(coor[1]) % self.data["tile_size"]) - (coor[1] - main_coor[1] * self.data["tile_size"]))

		# checking contact with other bricks
		for brick in bricks:
			if self.renderer.get_falling_brick().collide_vertical(brick):
				# stopping falling if collided with another brick
				self.renderer.get_falling_brick().stop_falling()

				# aligning with the collided brick
				self.renderer.get_falling_brick().align_with(main_coor[0] * self.data["tile_size"], round(coor[1]) - (round(coor[1]) % self.data["tile_size"]) - (coor[1] - main_coor[1] * self.data["tile_size"]))

	'''Checks horizontal collision with other bricks and aligns
	   with collided brick accordinly
	'''
	def check_horizontal_collision(self) -> None:
		pass

	'''Check brick collision both horizontal and vertical'''
	def check_collisions(self):
		if not self.renderer.get_falling_brick(): return
		self.check_vertical_collision()
		self.check_horizontal_collision()
		

