# editor

import json
import pygame as pg
from sys import exit
import customtkinter as ctk
from tkinter import colorchooser
from tkinter import filedialog
import os


SCREEN_SIZE = (600, 500)
TILE_SIZE = 50


class Prerequisite(ctk.CTkToplevel):

	def __init__(self):
		super().__init__()
		ctk.set_appearance_mode('dark')

		self.width = 400
		self.height = 300

		self.geometry(f'{self.width}x{self.height}+{(self.winfo_screenwidth() - self.width) // 2}+{(self.winfo_screenheight() - self.height) // 2}')
		self.resizable(False, False)
		self.title("Prerequisites")
		self.map = {}
		self.add_widgets()

		self.bind('<Escape>', lambda event: self.quit())
		self.mainloop()

	def add_widgets(self):
		font = ctk.CTkFont(family = 'Cascadia Mono', size = 15)
		self.path = ctk.StringVar(value = 'Enter Path')
		self.lvl = ctk.StringVar(value = "Enter Level Number")

		ctk.CTkLabel(self,
			text = 'Enter File Folder Path',
			font = font).pack(expand = True)

		frame = ctk.CTkFrame(self, fg_color = 'transparent')

		ctk.CTkEntry(frame,
			textvariable = self.path).place(relx = 0.1, rely = 0.5, relwidth = 0.6)
		ctk.CTkButton(frame,
			text = 'Browse',
			font = font,
			command = self.askfolder).place(relx = 0.65, rely = 0.5, relwidth = 0.3)
		frame.pack(expand = True, fill = 'both')

		self.lvl_entry = ctk.CTkEntry(self,
			font = font,
			textvariable = self.lvl)
		self.lvl_entry.pack(expand =  True)

		self.lvl_entry.bind('<Button-1>', lambda event: self.lvl.set(''))

		ctk.CTkButton(self,
			text = 'Load',
			font = font,
			command = self.load_map).pack(expand = True)

	def askfolder(self):
		path = filedialog.askdirectory()
		if path:
			self.path.set(path)

	def load_map(self):
		if not (os.path.exists(self.path.get()) and os.path.isdir(self.path.get())): return
		if not self.lvl.get().isdigit(): return
		if not os.path.exists(f'{self.path.get()}/{self.lvl.get()}.json'):
			temp = {}
			with open(f'{self.path.get()}/{self.lvl.get()}.json', 'w') as file:
				json.dump(temp, file)
		else:
			with open(f'{self.path.get()}/{self.lvl.get()}.json', 'r') as file:
				self.map = json.load(file)
		if not file.closed: file.close()
		self.quit()


class Editor(ctk.CTk):

	def __init__(self):
		super().__init__()

		self.geometry(f'{SCREEN_SIZE[0] + 200}x{SCREEN_SIZE[1]}+{(self.winfo_screenwidth() - (SCREEN_SIZE[0] + 200)) // 2}+{(self.winfo_screenheight() - SCREEN_SIZE[1]) // 2}')
		self.title("Level Editor")
		self.resizable(False, False)
		self.offset = [0, 0]
		self.tile_size = TILE_SIZE
		self.curr_color = 'gray'
		self.curr_phy_val = True
		self.map = {}
		self.rects = {}

		self.ask_input()
		
		ctk.set_appearance_mode('dark')

		if self.map: self.load_map_tiles()
		else: self.map = dict()

		self.bind('<Escape>', lambda event: self.quit())
		self.bind('<KeyPress>', self.change_offset)
		self.mainloop()

	def ask_input(self):
		pre = Prerequisite()
		pre.quit()
		self.map = pre.map
		self.lvl = pre.lvl.get()
		self.add_widgets()

	def load_map_tiles(self):
		for tile in self.map:
			semi_seen = False
			x = y = str()
			for ch in tile:
				if ch == ';': 
					semi_seen = True
					continue
				if not semi_seen: x += ch
				if semi_seen: y += ch
			pos = (int(x), int(y))
			self.rects[pos] = {'color' : self.map[tile]['color'], 'physics' : self.map[tile]['physics']}
		self.refresh()

	def change_offset(self, event):
		if event.char == 'w':
			self.offset[1] += 10
		if event.char == 's':
			self.offset[1] -= 10
		if event.char == 'a':
			self.offset[0] += 10
		if event.char == 'd':
			self.offset[0] -= 10
		self.refresh()

	def add_widgets(self):
		self.columnconfigure(0, weight = 2, uniform = 'a')
		self.columnconfigure(1, weight = 1, uniform = 'a')
		self.rowconfigure(0, weight = 1, uniform = 'a')

		self.canvas = ctk.CTkCanvas(self, bg = 'black')

		font = ctk.CTkFont(family = 'Cascadia Mono', size = 15)
		ioframe = ctk.CTkFrame(self)
		self.phy_var = ctk.StringVar(value = 'on')

		ctk.CTkSwitch(ioframe,
			text = "Physics Enabled",
			variable = self.phy_var,
			command = self.toogle_physics,
			onvalue = 'on',
			offvalue = 'off',
			font = font).pack(expand = True)

		ctk.CTkButton(ioframe,
			text = 'Choose Tile Color',
			font = font,
			command = self.choose_color).pack(expand = True)

		ctk.CTkButton(ioframe,
			text = "Save Changes",
			font = font,
			command = self.change_map).pack(expand = True)

		ioframe.grid(row = 0, column = 1, sticky = 'NSEW')

		self.canvas.grid(row = 0, column = 0, sticky = "NSEW")
		self.canvas.bind('<MouseWheel>', self.zoom)
		self.canvas.bind('<Button-1>', self.add_tile)
		self.canvas.bind('<Button-3>', self.remove_tile)

	def toogle_physics(self):
		if self.phy_var.get() == 'on': self.curr_phy_val = True
		else: self.curr_phy_val = False

	def choose_color(self):
		self.curr_color = colorchooser.askcolor()[1]

	def zoom(self, event):
		if event.delta > 0:
			self.tile_size = min(100, self.tile_size + 1)
		if event.delta < 0:
			self.tile_size = max(10, self.tile_size - 1)
		self.refresh()

	def refresh(self):
		self.canvas.delete('all')
		self.place_tiles()

	def place_tiles(self):
		for rect in self.rects:
			x = (rect[0] * self.tile_size) - self.offset[0]
			y = (rect[1] * self.tile_size) - self.offset[1]
			self.canvas.create_rectangle(x, y, x + self.tile_size, y + self.tile_size, fill = self.rects[rect]['color'])

	def get_tile_pos(self, x, y):
		return [int((x + self.offset[0]) // self.tile_size), int((y + self.offset[1]) // self.tile_size)]

	def add_tile(self, event):
		tile_pos = self.get_tile_pos(event.x, event.y)
		if tuple(tile_pos) not in self.rects:
			self.rects[tuple(tile_pos)] = {'color' : self.curr_color, 'physics' : self.curr_phy_val}
		self.refresh()

	def change_map(self):
		self.map.clear()
		for rect in self.rects:
			self.map.update({f'{rect[0]};{rect[1]}' : self.rects[rect]})
		with open(f'maps/{self.lvl}.json', 'w') as file:
			json.dump(self.map, file, sort_keys = True, indent = 4)
		if not file.closed: file.close()

	def remove_tile(self, event):
		tile_pos = self.get_tile_pos(event.x, event.y)
		if tuple(tile_pos) in self.rects:
			self.rects.pop(tuple(tile_pos))
		self.refresh()


if __name__ == '__main__':
	Editor()
