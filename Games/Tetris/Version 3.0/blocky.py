# this module defines blocky (the screen pet)

import pygame as pg
from animations import Animation, load_image


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
		self.delta = None
		self.curr_width = None
		self.box_ratio = 0.5 # i.e 2 : 1 ratio of width and height
		self.frames_elapsed = 0
		self.max_frames = 0
		self.min_width = 10
		self.min_height = 5
		self.anim_frames = self.game.settings["fps"] // 5
		self.max_height = None
		self.padding = 10
		self.max_text_surf_width = 200
		self.max_line_height = 15

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
		self.max_height = int((temp_rect.width / self.max_text_surf_width) * self.max_line_height) + 2 * self.padding
		self.curr_width = int(self.max_width * 0.25) # 25% of the total width
		self.delta = max((self.max_width - self.curr_width) // self.anim_frames, 1)

	# this function should not be called from outside the 
	# class definition, this one animates the text box
	def animate_box(self):
		self.frames_elapsed += 1
		if self.frames_elapsed >= self.max_frames:
			self.animate_shrink()
		else:
			self.animate_grow()

	# produces a growing animation
	def animate_grow(self):
		if not self.curr_width >= self.max_width:
			self.curr_width += self.delta

		x = self.x + 15
		y = self.y - (self.curr_width * self.box_ratio)

		self.box_surf = pg.transform.scale(self.text_box, (self.curr_width, self.curr_width * self.box_ratio))
		self.box_rect = self.box_surf.get_rect(topleft = (x, y))

	# produces a shrinking animation
	def animate_shrink(self):
		if self.curr_width > self.min_width:
			self.curr_width -= self.delta

		x = self.x + 15
		y = self.y - (self.curr_width * self.box_ratio)

		if self.curr_width <= self.min_width: 
			self.talking = False
			return

		self.box_surf = pg.transform.scale(self.text_box, (self.curr_width, self.curr_width * self.box_ratio))
		self.box_rect = self.box_surf.get_rect(topleft = (x, y))

