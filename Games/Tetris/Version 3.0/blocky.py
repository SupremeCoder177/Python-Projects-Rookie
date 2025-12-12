# this module defines blocky (the screen pet)

import pygame as pg
from animations import Animation, load_image
from typing import List


class Blocky:

	def __init__(self, game, x : int, y : int, tile_size : int, font : pg.font.Font, foreground : str):
		self.game = game
		self.x = x
		self.y = y
		self.tile_size = tile_size
		self.font = font
		self.fg = foreground

		# if you want to make custome animations then remember to change this path pls
		anim_path = "Images/Blocky Animations/"
		anim_duration = 15 # frames for each sprite

		# loading all the animations

		# state and animation mapping
		self.anim_map = {
			"idle" : Animation(anim_path + "blocky_idle.png", 32, anim_duration),
			"spin" : Animation(anim_path + "blocky_spin.png", 32, anim_duration)
		}

		# message vars
		# there a lot I know right (don't change them pls)
		self.text_box = load_image(anim_path + "text_box.png")
		self.box_surf = None
		self.box_rect = None
		self.max_width = None
		self.x_delta = None
		self.y_delta = None
		self.curr_width = None
		self.box_ratio = 0.5 # i.e 2 : 1 ratio of width and height
		self.frames_elapsed = 0
		self.max_frames = 0
		self.min_width = 10
		self.min_height = 5
		self.anim_frames = self.game.settings["fps"] // 5
		self.max_height = None
		self.padding = 15 # the text padding
		self.max_text_surf_width = 250
		self.text_size_ratio = 0.5
		self.max_line_height = self.game.settings["font_size"]
		self.message_surfs = []
		self.message_rects = []
		self.grow_complete = False

		# animation settings

		# state(s)
		self.state = "idle"
		self.changed_state = True
		self.talking = False

	# animates and draws blocky on the screen
	def draw(self):
		if self.changed_state:
			self.anim_map[self.state].reset()
			self.changed_state = False

		self.anim_map[self.state].update(self.game.frames_elapsed)
		self.anim_map[self.state].draw(self.x, self.y, self.game.screen, self.tile_size)

		# animating and drawing the text box
		if self.talking:
			self.animate_box()
			self.game.screen.blit(self.box_surf, self.box_rect)

			if self.grow_complete:
				for i in range(len(self.message_surfs)):
					self.game.screen.blit(self.message_surfs[i], self.message_rects[i])

	# changes current state of blocky to the state given
	def set_state(self, state : str):
		self.state = state if state in self.anim_map else self.state
		self.changed_state = True

	# makes blocky talk for the given amount of time (cool right)
	def send_message(self, text : str, time : int):
		self.talking = True
		self.frames_elapsed = 0
		self.max_frames = self.game.settings["fps"] * time
		temp = self.font.render(text, False, self.fg)
		temp_rect = temp.get_rect()

		self.max_width = self.max_text_surf_width + 2 * self.padding

		# making the message chunks
		words = text.split(" ")
		message_chunks = []
		chunk = []
		for word in words:		
			if self.get_chunk_length(chunk) + (len(word) * self.game.settings["font_size"]) <= self.max_text_surf_width:
				chunk.append(word)
			else:
				message_chunks.append(" ".join(chunk))
				chunk = [word]
		message_chunks.append(" ".join(chunk))

		self.max_height = len(message_chunks) * self.max_line_height + 2 * self.padding
		self.message_surfs = [self.font.render(message_chunks[i], False, self.fg) for i in range(len(message_chunks))]
		self.message_rects = [self.message_surfs[i].get_rect(topleft = (self.x + self.game.settings["blocky_text_x_pos"] + self.padding, self.y - self.max_height + (i * self.max_line_height) + self.padding)) for i in range(len(message_chunks))]

		self.curr_width = int(self.max_width * 0.25) # 25% of the total width
		self.curr_height = int(self.max_height * 0.15) # 15% of total height
		self.x_delta = max((self.max_width - self.curr_width) // self.anim_frames, 1)
		self.y_delta = max((self.max_height - self.curr_height) // self.anim_frames, 1)

	# this function should not be called from outside the 
	# class definition, this one animates the text box
	def animate_box(self):
		self.frames_elapsed += 1
		if self.frames_elapsed >= self.max_frames:
			self.grow_complete = False
			self.animate_shrink()
		else:
			self.animate_grow()

	# produces a growing animation
	def animate_grow(self):
		self.grow_complete = True
		if not self.curr_width >= self.max_width:
			self.curr_width += self.x_delta
			self.grow_complete = False

		if not self.curr_height >= self.max_height:
			self.curr_height += self.y_delta
			self.grow_complete = False

		x = self.x + self.game.settings["blocky_text_x_pos"]
		y = self.y - self.curr_height

		self.box_surf = pg.transform.scale(self.text_box, (self.curr_width, self.curr_height))
		self.box_rect = self.box_surf.get_rect(topleft = (x, y))

	# produces a shrinking animation
	def animate_shrink(self):
		if self.curr_width > self.min_width:
			self.curr_width -= self.x_delta

		if self.curr_height > self.min_height:
			self.curr_height -= self.y_delta

		x = self.x + self.game.settings["blocky_text_x_pos"]
		y = self.y - self.curr_height

		if self.curr_width <= self.min_width: 
			self.talking = False
			return

		self.box_surf = pg.transform.scale(self.text_box, (self.curr_width, self.curr_height))
		self.box_rect = self.box_surf.get_rect(topleft = (x, y))

	# returns the length of a message chunk
	def get_chunk_length(self, chunk : List[str]):
		return self.font.render(" ".join(chunk), False, self.fg).get_rect().width