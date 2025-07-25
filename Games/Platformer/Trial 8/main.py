# Platformer Trial 8

import pygame as pg
from sys import exit
from json import load, dump
from player import Player
from camera import Camera

class Game:

	def __init__(self):
		self.load_settings()
		pg.init()
		pg.display.set_caption(self.settings["game_name"])
		self.screen = pg.display.set_mode(self.settings["screen_size"])
		self.clock = pg.time.Clock()
		self.editor_mode = False
		self.offset_x, self.offset_y = 0, 0
		self.magnification = 1.0
		self.keys_held = set()
		self.released = set()
		self.grid_permi = False
		self.player = Player(self)
		self.camera = Camera(self, self.player)

	def load_settings(self):
		with open("settings.json", "r") as f:
			self.settings = load(f)

	def draw_grid(self):
		tile_size = int(self.settings["tile_size"] * self.magnification) if self.editor_mode else self.settings["tile_size"]
		for i in range(self.settings["screen_size"][0] // tile_size + 1):
			for j in range(self.settings["screen_size"][1] // tile_size + 1):
				pg.draw.rect(self.screen, 'grey', (i * tile_size, j * tile_size, tile_size, tile_size), 1)

	def move_map(self):
		keys = pg.key.get_pressed()
		speed = self.settings["edit_speed"]
		if self.editor_mode:
			if keys[pg.K_UP] or keys[pg.K_w]:
				self.offset_y += speed
			if keys[pg.K_DOWN] or keys[pg.K_s]:
				self.offset_y -= speed
			if keys[pg.K_LEFT] or keys[pg.K_a]:
				self.offset_x += speed
			if keys[pg.K_RIGHT] or keys[pg.K_d]:
				self.offset_x -= speed

	def draw_map(self):
		tile_size = int(self.settings["tile_size"] * self.magnification) if self.editor_mode else self.settings["tile_size"]
		for tile in self.settings["world_map"]:
			pg.draw.rect(self.screen, 'grey', (tile[0] * tile_size + self.offset_x, tile[1] * tile_size + self.offset_y, tile_size, tile_size))

	def run(self):
		while True:
			self.move_map()
			self.released.clear()
			for event in pg.event.get():
				if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
					pg.quit()
					exit()

				# toggling the editorial mode and grid permission
				if event.type == pg.KEYDOWN:
					self.keys_held.add(event.key)

					if pg.K_SPACE in self.keys_held and pg.K_e in self.keys_held:
						self.editor_mode = not self.editor_mode
						print("Editor Mode : ", self.editor_mode)
					if pg.K_SPACE in self.keys_held and pg.K_g in self.keys_held and self.editor_mode:
						self.grid_permi = not self.grid_permi
				if event.type == pg.KEYUP:
					self.keys_held.discard(event.key)
					self.released.add(event.key)

				# editor mode controls
				if self.editor_mode:

					# adding/removing tiles
					if event.type == pg.MOUSEBUTTONDOWN:
						pos = pg.mouse.get_pos()
						grid_pos = [(pos[0] - self.offset_x) // self.settings["tile_size"], (pos[1] - self.offset_y) // self.settings["tile_size"]]
						if pg.mouse.get_pressed()[0] and grid_pos not in self.settings["world_map"]:
							self.settings["world_map"].append(grid_pos)
						if pg.mouse.get_pressed()[2]:
							if grid_pos in self.settings["world_map"]:
								self.settings["world_map"].remove(grid_pos)

					# saving changes
					if event.type == pg.KEYDOWN and event.key == pg.K_LCTRL:
						with open("settings.json", 'w') as f:
							dump(self.settings, f, sort_keys=False, indent=4)

					# deleting everything
					if event.type == pg.KEYDOWN and event.key == pg.K_DELETE:
						self.settings["world_map"] = []

					# zooming
					if event.type == pg.MOUSEWHEEL:
						self.magnification += 0.1 if event.y > 0 else -0.1
						self.magnification = max(0.5, self.magnification)

					# changing tile size
					if event.type == pg.MOUSEWHEEL:
						if pg.K_SPACE in self.keys_held:
							self.settings["tile_size"] += 1 if event.y > 0 else -1
							self.settings["tile_size"] = max(20, self.settings["tile_size"])

					# changing perspective offset to 0
					if event.type == pg.KEYDOWN and event.key == pg.K_0:
						self.offset_x, self.offset_y = 0, 0

			# clearing screen
			self.screen.fill("#121212") 

			# drawing on screen
			self.draw_grid() if self.grid_permi else None
			self.draw_map()
			if not self.editor_mode:
				self.player.draw()

			#updating player
			if not self.editor_mode:
				self.player.update()
				self.camera.update()
			
			# updating screen
			pg.display.flip()
			self.clock.tick(self.settings["fps"])

if __name__ == '__main__':
	game = Game()
	game.run()