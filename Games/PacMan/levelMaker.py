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
		self.tile_size = TILE_SIZE
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

		self.current_sprite_surf = list(self.sprites[self.current_sprite].values())[0]
		self.current_sprite_type = list(self.sprites[self.current_sprite].keys())[0]
		self.current_sprite_rect = self.current_sprite_surf.get_rect(topleft=(SCREEN_SIZE[0] - self.current_sprite_surf.get_width() + 10, 10))

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
		if "enemy_postions" not in keys:
			self.level_file["enemy_postions"] = []

		if "coin_positions" not in keys:
			self.level_file["coin_positions"] = []

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

	def draw_entities(self):
		pass

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

					# changing current chosen sprite or changing magnification (Left Ctrl + mousewheel to change magnification)
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
						tile_pos = mouse_pos[0] // self.tile_size, mouse_pos[1] // self.tile_size
						str_pos = f'{tile_pos[0]},{tile_pos[1]}'
						if pg.mouse.get_pressed()[0] and str_pos not in self.level_file["world_map"].keys():
							self.level_file["world_map"][str_pos] = self.current_sprite_type
						if pg.mouse.get_pressed()[2] and str_pos in self.level_file["world_map"].keys():
							del self.level_file["world_map"][str_pos]

					# saving changes to file
					# (its q because s is being used to change y offset)
					if event.type == pg.KEYDOWN and event.key == pg.K_q:
						self.save()

			if self.running:
				# clearing the screen
				self.screen.fill('#121212')

				# taking inputs for offset changes
				self.take_continous_input()

				# drawing the walls and entities
				self.draw_walls()
				self.draw_entities()

				# displaying the currently selected sprite on the topright corner of the screen
				self.screen.blit(self.current_sprite_surf, self.current_sprite_rect)
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
	LevelMaker().run()