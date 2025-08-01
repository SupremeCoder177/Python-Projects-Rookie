# Collision Manager

from settings import *
from random import choice

class Collisions:

	def __init__(self, game):
		self.game = game
		self.occupied_tiles = {}

	def update(self):
		self.update_entity_tiles()

		if self.check_player_wall_collision():
			self.change_player_direction(collided=True)

		self.check_enemy_wall_collision()
		for enemy_type in self.game.enemy_manager.enemy_info:
			if enemy_type in self.game.enemy_manager.collided_ones:
				self.change_enemy_direction(enemy_type, collided=True)
			else:
				self.change_enemy_direction(enemy_type)
		self.occupied_tiles = {}

	def check_player_wall_collision(self):
		player = self.game.player
		pos = player.pos
		direction = player.direction
		temp = PLAYER_PROJECTED_MULTIPLIER
		front_points = None
		if direction == "left":
			front_points = [[pos[0], pos[1]], [pos[0], pos[1] + temp]]
		if direction == "right":
			front_points = [[pos[0] + temp, pos[1]], [pos[0] + temp, pos[1] + temp]]
		if direction == "up":
			front_points = [[pos[0], pos[1]], [pos[0] + temp, pos[1]]]
		if direction == "down":
			front_points = [[pos[0], pos[1] + temp], [pos[0] + temp, pos[1] + temp]]

		for point in front_points:
			if self.game.level_loader.is_blocked(point):
				return True
		return False

	def change_player_direction(self, collided=False):
		# changing player direction due to collision to a wall
		player = self.game.player
		pos = player.pos
		direction = player.direction

		# stoppig player at wall
		if collided:
			dx = player.directional_speed_map[direction][0]  * self.game.delta_time
			dy = player.directional_speed_map[direction][1]  * self.game.delta_time
			self.game.player.pos[0] -= dx
			self.game.player.pos[1] -= dy

		directions = self.get_available_direction(self.game.player.get_tile_pos())
		if OPP_MAP[direction] in directions: directions.remove(OPP_MAP[direction])
		if not directions and collided:
			self.game.player.direction = OPP_MAP[direction]
		else:
			if self.game.player.next_direction in directions and not collided:
				self.game.player.direction = self.game.player.next_direction
				self.game.player.next_direction = ""
			else:
				self.game.player.direction = choice(directions)

	def change_enemy_direction(self, type_, collided=False):
		manager = self.game.enemy_manager
		pos = manager.enemy_info[type_]
		index = 0
		for _type in manager.enemy_info:
			if manager.enemy_info[_type] == pos:
				break
			index += 1
		direction = manager.directions[index]

		# stopping enemy at wall
		if collided:
			dx = manager.directional_speed_map[direction][0] * self.game.delta_time
			dy = manager.directional_speed_map[direction][1] * self.game.delta_time
			self.game.enemy_manager.enemy_info[type_][0] -= dx
			self.game.enemy_manager.enemy_info[type_][1] -= dy

		directions = self.get_available_direction(manager.get_tile_pos(type_))
		if OPP_MAP[direction] in directions: directions.remove(OPP_MAP[direction])
		if not directions:
			self.game.enemy_manager.directions[index] = OPP_MAP[direction]
		else:
			# now things become ineteresting here
			# distances = {}
			# for direction in directions:
			# 	temp = pos
			# 	temp[0] += DIRECTIONAL_ADDER[direction][0]
			# 	temp[1] += DIRECTIONAL_ADDER[direction][1]
			# 	dist = self.calc_dist(temp, self.occupied_tiles["player"])
			# 	distances[dist] = direction
			# self.game.enemy_manager.directions[index] = distances[min(list(distances.keys()))]
			self.game.enemy_manager.directions[index] = choice(directions)
		if collided:
			self.game.enemy_manager.collided_ones.remove(type_)

	# the position argument must be a tile position not a map position
	def get_available_direction(self, pos):
		directions = []
		if not self.game.level_loader.is_blocked((pos[0] - 1, pos[1])):
			directions.append("left")
		if not self.game.level_loader.is_blocked((pos[0] + 1, pos[1])):
			directions.append("right")
		if not self.game.level_loader.is_blocked((pos[0], pos[1] - 1)):
			directions.append("up")
		if not self.game.level_loader.is_blocked((pos[0], pos[1] + 1)):
			directions.append("down")
		return directions

	def check_enemy_wall_collision(self):
		for i in range(len(self.game.enemy_manager.directions)):
			pos = list(self.game.enemy_manager.enemy_info.values())[i]
			type_ = list(self.game.enemy_manager.enemy_info.keys())[i]
			direction = self.game.enemy_manager.directions[i]
			temp = ENEMY_PROJECTED_MULTIPLIER

			front_points = None
			if direction == "left":
				front_points = [[pos[0], pos[1]], [pos[0], pos[1] + temp]]
			if direction == "right":
				front_points = [[pos[0] + temp, pos[1]], [pos[0] + temp, pos[1] + temp]]
			if direction == "up":
				front_points = [[pos[0], pos[1]], [pos[0] + temp, pos[1]]]
			if direction == "down":
				front_points = [[pos[0], pos[1] + temp], [pos[0] + temp, pos[1] + temp]]

			for point in front_points:
				if self.game.level_loader.is_blocked(point):
					self.game.enemy_manager.collided_ones.append(type_)

	def update_entity_tiles(self):
		self.occupied_tiles["player"] = self.game.player.get_tile_pos()
		count = 0
		for type_ in self.game.enemy_manager.enemy_info:
			self.occupied_tiles[f"enemy{count}"] = self.game.enemy_manager.get_tile_pos(type_)

	def calc_dist(self, point1, point2):
		return (abs(point1[0] - point2[0]) ** 2 + abs(point1[1] - point2[1]) ** 2) ** (1/2)

	def check_enemy_player_collision(self):
		pass

