# Working version of tetris 2.0

import pygame as pg
from json import load, dump
from os import listdir, getcwd
from sys import exit
from random import randint
from brick import *
from handler import Handler
from widgets import Button
from sound import Sounds

# exiting if json file not in cwd
if not "settings.json" in listdir(getcwd()):
	exit()

# loading settings from json file in project folder
with open("settings.json", 'r') as f:
	DATA = load(f)


class Game:

	def __init__(self, data):
		pg.init()
		self.data = data
		self.screen = pg.display.set_mode(self.data["screen_size"])
		pg.display.set_caption(self.data["game_name"])
		self.clock = pg.time.Clock()
		self.manager = BricksManager(self, self.screen, self.data)
		self.handler = Handler(self, self.manager)
		self.manager.add_brick()
		self.timer = 1 / self.data["brick_fall_speed"]
		self.input_timer = 0.3
		self.last_update_time = 0
		self.last_handle_time = 0
		self.btn_font = pg.font.Font("Fonts/StayPixel.ttf", 40)
		self.score_font = pg.font.Font("Fonts/Chalice.ttf", 20)
		self.ui_init()
		self.running = False
		self.paused = False
		self.played_once = False
		self.last_bgm_time = 0
		self.score = 0
		self.lvl = 1
		Sounds.play_bgm()

	# method to draw a grid on the screen
	def draw_grid(self):
		x_offset = self.data["grid_x_offset"]
		y_offset = self.data["grid_y_offset"]
		grid_size = self.data["grid_size"]
		tile_size = self.data["tile_size"]
		colour = self.data["grid_color"]

		for i in range(grid_size[0] // tile_size):
			for j in range(grid_size[1] // tile_size):
				pg.draw.rect(self.screen, colour, (i * tile_size, j * tile_size, tile_size, tile_size), 1)

	def check_lvl_up(self):
		if self.score == 0: return
		if self.score -  self.lvl * self.data["level_up_mark"] > 0:
			self.lvl += 1
			Sounds.level_up()
		
	def check_line(self):
		rows = self.data["grid_size"][0] // self.data["tile_size"] 
		columns = self.data["grid_size"][0] // self.data["tile_size"]
		for i in range(rows):
			full_line = True
			for j in range(columns):
				if not (j * self.data["tile_size"], i * self.data["tile_size"]) in self.manager.get_occupied():
					full_line = False
					break
			if full_line:
				self.manager.move_down_occupied(i)
				Sounds.full_line()

		self.check_lvl_up()

	def reset_timer(self):
		self.timer = 1 / self.data["brick_fall_speed"]
		Sounds.block_fall()

	def ui_init(self):
		self.play_btn = Button(self.screen, "Play", "#151ec2", "#9395b8", "#0c1175", self.btn_font, self.data["play_btn_pos"][0], self.data["play_btn_pos"][1], self.data["play_btn_dimensions"][0], self.data["play_btn_dimensions"][1])
		self.pause_btn = Button(self.screen, "Pause", "#151ec2", "#9395b8", "#0c1175", self.btn_font, self.data["pause_btn_pos"][0], self.data["pause_btn_pos"][1], self.data["pause_btn_dimensions"][0], self.data["pause_btn_dimensions"][1])
		self.restart_btn = Button(self.screen, "Restart", "#151ec2", "#9395b8", "#0c1175", self.btn_font, self.data["restart_btn_pos"][0], self.data["restart_btn_pos"][1], self.data["restart_btn_dimensions"][0], self.data["restart_btn_dimensions"][1])

	def draw_ui(self):
		self.play_btn.render()
		self.pause_btn.render()
		self.restart_btn.render()

		score_surf = self.score_font.render(f'Score\n{self.score}', False, self.data["score_color"])
		score_rect = score_surf.get_rect(topleft = self.data["score_rect_pos"])

		high_score_surf = self.score_font.render(f'High Score:\n{self.data["high_score"]}', False, self.data["score_color"])
		high_score_rect = high_score_surf.get_rect(topleft = self.data["high_score_pos"])

		lvl_surf = self.score_font.render(f"Level\n{self.lvl}", False, self.data["score_color"])
		lvl_rect = lvl_surf.get_rect(topleft = self.data["level_up_pos"])

		self.screen.blit(score_surf, score_rect)
		self.screen.blit(high_score_surf, high_score_rect)
		self.screen.blit(lvl_surf, lvl_rect)

	def check_over(self):
		if self.manager.get_min_y() <= 0 and self.manager.check_brick_offset(self.manager.curr_brick):

			self.running = False
			self.paused = False
			self.score = 0
			self.lvl = 1
			self.manager.delete_all()
			Sounds.game_over()

	def update_ui(self):
		self.play_btn.update()
		self.pause_btn.update()
		if self.played_once: self.restart_btn.update()

	def update_high_score(self):
		with open("settings.json", 'w')  as file:
			self.data["high_score"] = self.score
			dump(self.data, file, indent = 4)

	# method to run the main game window
	def run(self):
		while True:

			for event in pg.event.get():
				if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
					pg.quit()
					exit()
				if self.running:
					self.handler.change_input_state(event)

				if self.play_btn.clicked(event):
					self.running = True
					self.played_once = True
					self.paused = False

				if self.pause_btn.clicked(event) and self.played_once:
					self.running = False
					self.paused = True

				if self.restart_btn.clicked(event) and self.played_once:
					self.running = False
					self.paused = False
					self.played_once = False
					self.score = 0
					self.manager.delete_all()

			# clearing the screen
			self.screen.fill(self.data["game_bg"])

			# drawing a grid
			self.draw_grid()

			# drawing the ui
			self.draw_ui()

			# updatig the ui
			self.update_ui()

			if self.running:
				current_time = pg.time.get_ticks() / 1000

				#bgm updates
				if current_time - self.last_bgm_time >= Sounds.curr_bgm_len():
					Sounds.play_bgm()
					self.last_bgm_time = current_time

				# logic updates
				if current_time - self.last_update_time >= self.timer:
					self.manager.update()
					self.last_update_time = current_time
				if current_time - self.last_handle_time >= self.input_timer:
					self.handler.handle()
					self.last_handle_time = current_time

				self.check_over()

				# checking is new high score is reached
				if self.score > self.data["high_score"]:
					self.update_high_score()

			# rendeting updates
			if self.running or (not self.running and self.paused):
				self.manager.render()

				# checking line
				self.check_line()

			# updating the screen
			pg.display.flip()
			self.clock.tick(self.data["fps"])


if __name__ == '__main__':
	game = Game(DATA)
	game.run()