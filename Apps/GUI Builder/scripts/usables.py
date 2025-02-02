# usable custom widgets

import customtkinter as ctk
from time import sleep, time


class SliderFrame(ctk.CTkFrame):

	def __init__(self, parent, fg_color, llm, ulm, btn_clr, btn_hvr_clr, progress_clr, font, var, var_name):
		super().__init__(master = parent, fg_color = fg_color)
		self.rowconfigure((0, 1), weight = 1, uniform = 'b')
		self.columnconfigure((0, 1), weight = 1, uniform = 'b')
		self.temp = ctk.CTkLabel(self,
			fg_color = 'transparent',
			font = font,
			text = var.get())
		self.temp.grid(row = 1, column = 1, sticky = 'NSEW')
		ctk.CTkSlider(self,
			from_ = llm,
			to = ulm,
			button_color = btn_clr,
			button_hover_color = btn_hvr_clr,
			progress_color = progress_clr,
			variable = var,
			command = self.change_text,
			number_of_steps = ulm - llm).grid(row = 0, column = 0, columnspan = 2, sticky = 'NSEW')
		ctk.CTkLabel(self,
			fg_color = 'transparent',
			font = font,
			text = var_name).grid(row = 1, column = 0, sticky = 'NSEW')

	def change_text(self, var):
		self.temp.configure(text = var)


class AnimatedPanel(ctk.CTkFrame):

	def __init__(self, parent, start, end, coor_other, orient, width, height, bg, btn_text, btn_text_after, btn_clr, btn_hvr_clr, btn_width, btn_ht):
		self.start = start
		self.end = end
		self.x = self.start if orient == 'horizontal' else coor_other
		self.y = self.start if orient == 'vertical' else coor_other
		self.at_start = True
		self.width = width
		self.height = height
		self.orient = orient
		self.inc = 0.01
		self.offset = 0.01
		self.btn_txt = btn_text
		self.btn_txt_after = btn_text_after
		super().__init__(master = parent, fg_color = bg)

		if orient == 'horizontal':
			if start > end: 
				btn_x = 1 - btn_width
			else: 
				btn_x = 0
			btn_y = 0
		else:
			if start > end: 
				btn_y = 1 - btn_ht
			else:
				btn_y = 0
			btn_x = 0

		self.btn = ctk.CTkButton(self,
			text = btn_text,
			fg_color = btn_clr,
			hover_color = btn_hvr_clr,
			command = self.animate)
		self.btn.place(relx = btn_x, rely = btn_y, relwidth = btn_width, relheight = btn_ht, anchor = 'nw')
		self.update()

	def update(self):
		if self.orient == 'horizontal' and self.start > self.end:
			self.place(relx = self.x, rely = self.y, relwidth = self.width, relheight = self.height, anchor = 'ne')
		if self.orient == 'horizontal' and self.start < self.end:
			self.place(relx = self.x, rely = self.y, relwidth = self.width, relheight = self.height)
		if self.orient == 'vertical' and self.start < self.end:
			self.place(relx = self.x, rely = self.y, relwidth = self.width, relheight = self.height)
		if self.orient == 'vertical' and self.start > self.end:
			self.place(relx = self.x, rely = self.y, relwidth = self.width, relheight = self.height, anchor = 'sw')

	def animate(self):
		if self.at_start: self.animate_back()
		else: self.animate_front()

	def animate_back(self):
		if self.orient == 'horizontal':
			self.x += self.inc if self.start < self.end else -self.inc
			self.update()
			if not self.end - self.offset <= self.x <= self.end + self.offset: self.after(10, self.animate_back)
			else: 
				self.at_start = False
				self.btn.configure(text = self.btn_txt_after)
		else:
			self.y += self.inc if self.start < self.end else -self.inc
			self.update()
			if not self.end - self.offset <= self.y <= self.end + self.offset: self.after(10, self.animate_back)
			else: 
				self.at_start = False
				self.btn.configure(text = self.btn_txt_after)

	def animate_front(self):
		if self.orient == 'horizontal':
			self.x += self.inc if self.end < self.start else -self.inc
			self.update()
			if not self.start - self.offset <= self.x <= self.start + self.offset: self.after(10, self.animate_front)
			else: 
				self.at_start = True
				self.btn.configure(text = self.btn_txt)
		else:
			self.y += self.inc if self.end < self.start else -self.inc
			self.update()
			if not self.start - self.offset <= self.y <= self.start + self.offset: self.after(10, self.animate_front)
			else: 
				self.at_start = True
				self.btn.configure(text = self.btn_txt)


class SingleCustom(ctk.CTkFrame):

	def __init__(self, parent, bg, custom_name, custom_type, place=True):
		super().__init__(master = parent, fg_color = bg)
		if place: self.pack(expand = True)


