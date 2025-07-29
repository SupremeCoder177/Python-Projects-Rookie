# To Make Levels for Pac Man

# WARNING : For some reason you cannot exit until you enter
#			a level in the CLI, no matter what I do it doesn't
# 			let me exit and goes into (not responding) mode
#			also don't click on the pygame window until you have 
# 			entered a level path in CLI

import pygame as pg
from sys import exit
from json import load, dump
from graphicsLoader import Load
from settings import *
import os

class LevelMaker:

	def __init__(self):
		pg.init()
		pg.display.set_caption("PacMan Level Maker")
		self.running = False
		self.tile_size = int(TILE_SIZE)
		self.level_file = None
		self.path = ""
		self.screen = pg.display.set_mode(SCREEN_SIZE)
		self.clock = pg.time.Clock()
		self.offset_x = self.offset_y = 0
		self.loader = Load()
		self.sprites_total = self.loader.sprites_total
		self.sprites = self.loader.sprites
		self.current_sprite = 0
		self.delta_time = 1
		self.player_added = False
		self.enemy_count = 0
		self.max_enemy = 4
		self.grid = False

		self.current_sprite_surf = list(self.sprites[self.current_sprite].values())[0]
		self.current_sprite_type = list(self.sprites[self.current_sprite].keys())[0]
		self.current_sprite_rect = self.current_sprite_surf.get_rect(topleft=(SCREEN_SIZE[0] - (self.current_sprite_surf.get_width() * 2), 10))

	# loads data from the json file, should only be called when running = False
	# and then adds the default things if not present already in the file
	def load_file(self):
		with open(self.path, 'r') as f:
			self.level_file = load(f)

		keys = self.level_file.keys()

		# checking if pre-built world map is present in the file
		if "world_map" not in keys:
			self.level_file["world_map"] = {}

		# checking player position is in the file 
		if "player_pos" not in keys:
			self.level_file["player_pos"] = []

		# checking if enemy positions are present in the file
		if "enemy_info" not in keys:
			self.level_file["enemy_info"] = {}

		if "coin_positions" not in keys:
			self.level_file["coin_positions"] = []

		self.enemy_count = len(self.level_file["enemy_info"])
		if self.level_file["player_pos"]:
			self.player_added = True
		
		self.save()

	def draw_walls(self):
		for tile in self.level_file["world_map"]:
			x, y = tile.split(',')
			pos = int(x) * self.tile_size + self.offset_x, int(y) * self.tile_size + self.offset_y
			sprite_type = self.level_file["world_map"][tile]
			sprite = None
			for index, type in self.sprites.items():
				if sprite_type in type:
					sprite = list(type.values())[0]
			self.screen.blit(sprite, pos)

	# draws a grid
	def draw_grid(self):
		for i in range(SCREEN_SIZE[0] // self.tile_size):
			for j in range(SCREEN_SIZE[1] // self.tile_size):
				pg.draw.rect(self.screen, 'grey', (i * self.tile_size, j * self.tile_size, self.tile_size, self.tile_size), 1)


	def draw_entities(self):
		# player
		if self.player_added:
			surf = None
			for index, surf_type in self.sprites.items():
				if list(surf_type.keys())[0].startswith("player"):
					surf = list(self.sprites[index].values())[0]
					break
			pos = self.level_file["player_pos"][0] * self.tile_size + self.offset_x, self.level_file["player_pos"][1] * self.tile_size + self.offset_y
			self.screen.blit(surf, pos)

		# enemies
		for type, pos in self.level_file["enemy_info"].items():
			surf = None
			for index, surf_type in self.sprites.items():
				if list(surf_type.keys())[0] == type:
					surf = list(self.sprites[index].values())[0]
			map_pos = pos[0] * self.tile_size + self.offset_x, pos[1] * self.tile_size + self.offset_y
			self.screen.blit(surf, map_pos)

	# save changed to the json file
	def save(self):
		with open(self.path, 'w') as f:
			dump(self.level_file, f, indent = 4, sort_keys = True)

	def change_chosen_sprite(self):
		self.current_sprite_surf = list(self.sprites[self.current_sprite].values())[0]
		self.current_sprite_type = list(self.sprites[self.current_sprite].keys())[0]

	# only for chaning offset 
	def take_continous_input(self):
		keys = pg.key.get_pressed()

		if keys[pg.K_a]:
			self.offset_x += OFFSET_CHANGE_SPEED * self.delta_time
		if keys[pg.K_d]:
			self.offset_x -= OFFSET_CHANGE_SPEED * self.delta_time
		if keys[pg.K_w]:
			self.offset_y += OFFSET_CHANGE_SPEED * self.delta_time
		if keys[pg.K_s]:
			self.offset_y -= OFFSET_CHANGE_SPEED * self.delta_time


	def run(self):
		while True:
			for event in pg.event.get():
				if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
					pg.quit()
					exit()
				if self.running:

					# changing current chosen sprite
					if event.type == pg.MOUSEWHEEL:
						self.current_sprite += 1 if event.y > 0 else -1
						self.current_sprite = self.sprites_total - 1 if self.current_sprite < 0 else self.current_sprite
						self.current_sprite = 0 if self.current_sprite >= self.sprites_total else self.current_sprite
						self.change_chosen_sprite()

					# adding walls and entities 
					# Also the reason I am using str_pos as the key for wall tiles and not
					# simply tile_pos is because in json you cannot have
					# tuples or list as keys
					if event.type == pg.MOUSEBUTTONDOWN:
						mouse_pos = pg.mouse.get_pos()
						tile_pos = int((mouse_pos[0] - self.offset_x) / self.tile_size), int((mouse_pos[1] - self.offset_y) / self.tile_size)
						str_pos = f'{tile_pos[0]},{tile_pos[1]}'
						if self.current_sprite_type.startswith("wall"):
							if pg.mouse.get_pressed()[0] and str_pos not in self.level_file["world_map"].keys():
								self.level_file["world_map"][str_pos] = self.current_sprite_type
							if pg.mouse.get_pressed()[2] and str_pos in self.level_file["world_map"].keys():
								del self.level_file["world_map"][str_pos]

						if self.current_sprite_type.startswith("player"):
							if pg.mouse.get_pressed()[0] and str_pos not in self.level_file["world_map"] and not self.player_added:
								self.level_file["player_pos"] = tile_pos
								self.player_added = True
							if pg.mouse.get_pressed()[2] and tile_pos[0] == self.level_file["player_pos"][0] and tile_pos[1] == self.level_file["player_pos"][1]:
								self.level_file["player_pos"] = []
								self.player_added = False

						if self.current_sprite_type.startswith("enemy"):
							if pg.mouse.get_pressed()[0] and str_pos not in self.level_file["world_map"] and self.enemy_count < self.max_enemy and tile_pos not in self.level_file["enemy_info"].values():
								self.enemy_count += 1
								self.level_file["enemy_info"][self.current_sprite_type] = tile_pos
							if pg.mouse.get_pressed()[2] and list(tile_pos) in self.level_file["enemy_info"].values():
								temp = ""
								for type, pos in self.level_file["enemy_info"].items():
									if pos == list(tile_pos):
										temp = type
										self.enemy_count -= 1
										break
								del self.level_file["enemy_info"][temp]

					# saving changes to file
					# (its q because s is being used to change y offset)
					if event.type == pg.KEYDOWN and event.key == pg.K_q:
						self.save()

					# toggling the drawing of grid
					if event.type == pg.KEYDOWN and event.key == pg.K_g:
						self.grid = not self.grid

			if self.running:
				# clearing the screen
				self.screen.fill('#121212')

				# taking inputs for offset changes
				self.take_continous_input()

				#drawing grid if turned on
				if self.grid:
					self.draw_grid()

				# drawing the walls and entities
				self.draw_walls()
				self.draw_entities()

				# displaying the currently selected sprite on the topright corner of the screen
				surf = pg.transform.scale2x(self.current_sprite_surf)
				self.screen.blit(surf, self.current_sprite_rect)
			else:
				# asking to open the json file to make the level
				# the file should either be empty or only altered by this program only
				# if the json file contains some other data not related to the level
				# the main.py file will ignore it, but it can cause errors if some ignored
				# key values share the same name as the ones pre-programmed in this class
				print("Enter 0 to exit\nIf the name of the file entered does not exit, one will be made")
				temp = input("Enter path to json file:")
				if temp == "0":
					pg.quit()
					exit()
				if os.path.exists(temp) and temp.endswith(".json"):
					self.path = temp
					self.running = True
					self.load_file()

				# checking if the user wants to create a new json file from the CLI
				else:
					head, tail = os.path.split(temp)
					if os.path.exists(head):
						if tail.endswith(".json"):
							with open(temp, 'w') as f: 
								dump({}, f)
							self.path = temp
							self.running = True
							self.load_file()
						else:
							print("File name must end in .json to be created !!")
					else:
						print("Path does not exist !!")

			pg.display.flip()
			self.delta_time = self.clock.tick(FPS) / 100



if __name__ == '__main__':
	a = LevelMaker()
	a.run()