# Sound handler

import pygame as pg
import os


class Sounds:

	pg.mixer.init()

	audio = {}

	for file in os.listdir("Sounds/"):
		audio[file[:file.index(".")]] = pg.mixer.Sound(os.path.join("Sounds/", file))

	bgm_map = {
	 0 : "bgm1",
	 1 : "bgm2",
	 2 : "bgm3"
	}

	curr_bgm = 0

	max_bgm = len(bgm_map) - 1

	@classmethod
	def play_bgm(cls):
		cls.audio[cls.bgm_map[cls.curr_bgm]].play(1)
		cls.curr_bgm += 1
		if cls.curr_bgm > cls.max_bgm:
			cls.curr_bgm = 0

	@classmethod
	def stop_bgm(cls):
		cls.audio[cls.bgm_map[cls.curr_bgm]].stop()

	@classmethod
	def full_line(cls):
		cls.audio["full_line"].play(1)

	@classmethod
	def block_fall(cls):
		cls.audio["block_fall"].play(1)

	@classmethod
	def level_up(cls):
		cls.audio["level_up"].play(1)

	@classmethod
	def game_over(cls):
		cls.audio["game_over"].play(1)

	@classmethod
	def curr_bgm_len(cls):
		return cls.audio[cls.bgm_map[cls.curr_bgm]].get_length()