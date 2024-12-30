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


class SingleAttribute(ctk.CTkFrame):

		def __init__(self, parent, bg, pad, attribute_name, val, font, app):
			super().__init__(parent, fg_color = bg)

			self.rowconfigure((0, 1), weight = 1, uniform = 'b')
			self.columnconfigure((0, 1), weight = 1, uniform = 'b')
			self.app = app
			self.attribute_name = attribute_name
			self.val = ctk.StringVar(value = str(val))

			ctk.CTkLabel(self,
				text = attribute_name.capitalize(),
				font = font,
				fg_color = 'transparent').grid(row = 0, column = 0, sticky = 'NSEW')

			ctk.CTkLabel(self,
				text = str(val),
				font = font,
				fg_color = 'transparent',
				textvariable = self.val).grid(row = 0, column = 1, sticky = 'NSEW')

			if type(val) == bool:
				self.bool_var = ctk.StringVar()
				ctk.CTkSwitch(self,
					text = f'{attribute_name.capitalize()} Enable',
					command = self.change_bool,
					font = font,
					variable = self.bool_var,
					onvalue = 'on',
					offvalue = 'off').grid(row = 1, column = 0, columnspan = 2, sticky = 'NSEW')
			else:
				ctk.CTkButton(self,
					text = "Choose Color",
					font = font,
					command = self.change_color).grid(row = 1, column = 0, columnspan = 2, sticky = 'NSEW')

			self.pack(padx = pad, pady = pad, expand = True, fill = 'both')

		def change_bool(self):
			if self.bool_var.get() == 'on': 
				self.app.attributes[self.attribute_name] = True
				self.val.set('True')
			else: 
				self.app.attributes[self.attribute_name] = False
				self.val.set('False')

		def change_color(self):
			color = colorchooser.askcolor()[1]
			if color:
				self.app.attributes[self.attribute_name] = color
				self.val.set(color)


class Editor(ctk.CTk):

	def __init__(self):
		super().__init__()

		self.geometry(f'{SCREEN_SIZE[0] + 200}x{SCREEN_SIZE[1]}+{(self.winfo_screenwidth() - (SCREEN_SIZE[0] + 200)) // 2}+{(self.winfo_screenheight() - SCREEN_SIZE[1]) // 2}')
		self.title("Level Editor")
		self.resizable(False, False)
		self.offset = [0, 0]
		self.tile_size = TILE_SIZE
		self.map = {}
		self.rects = {}
		self.attributes = {"physics" : True, "color" : 'gray'}

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
		if not pre.map: self.quit()
		self.map = pre.map
		self.lvl = pre.lvl.get()
		self.path = pre.path.get()
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

		# input field

		self.tabs = ctk.CTkTabview(self, fg_color = 'transparent')
		self.tabs.add('Attributes')
		self.tabs.add('Save')
		self.tabs.grid(row = 0, column = 1, sticky = 'NSEW')
		self.attributes_widgets()

		ctk.CTkButton(self.tabs.tab('Save'),
			text = 'Save Changes',
			font = ("Cascadia Mono", 20),
			command = self.save_map).pack(expand = True)

		self.canvas = ctk.CTkCanvas(self, bg = 'black')
		self.canvas.grid(row = 0, column = 0, sticky = "NSEW")
		self.canvas.bind('<MouseWheel>', self.zoom)
		self.canvas.bind('<Button-1>', self.add_tile)
		self.canvas.bind('<Button-3>', self.remove_tile)

	def save_map(self):
		self.map.clear()
		for rect in self.rects:
			self.map[f'{rect[0]};{rect[1]}'] = self.rects[rect]
		with open(f'{self.path}/{self.lvl}.json', 'w') as file:
			json.dump(self.map, file, indent = 4, sort_keys = True)

	def attributes_widgets(self):
		for widget in self.tabs.tab('Attributes').winfo_children():
			widget.destroy()

		frame = ctk.CTkScrollableFrame(self.tabs.tab("Attributes"))

		frame.pack(expand = True, fill = 'both')
		font = ctk.CTkFont(family = 'Cascadia Mono', size = 15)
		for attribute in self.attributes:
			SingleAttribute(frame, '#0f0f0f', 10, attribute, self.attributes[attribute], font, self)

		ctk.CTkButton(frame,
			text = '+',
			font = ("Cascadia Mono", 25),
			width = 50,
			height = 50,
			command = self.add_attribute).pack(expand = True, pady = 10, padx = 10)

	def add_attribute(self):
		window = ctk.CTkToplevel(self)
		window.title("Add attribute")
		window.geometry('350x200')

		font = ctk.CTkFont(family = 'Cascadia Mono', size = 15)
		name = ctk.StringVar(value = 'Enter Name')

		ctk.CTkLabel(window,
			text = "Enter attribute name (Single Letter)",
			font = font).pack(expand = True)

		ctk.CTkEntry(window,
			textvariable = name,
			font = font).pack(expand = True, fill = 'x', padx = 10, pady = 10)

		ctk.CTkButton(window,
			text = 'Add',
			font = font,
			command = lambda: self.add(name)).pack(expand = True, padx = 10)

		window.bind('<Escape>', lambda event: window.quit())
		window.mainloop()

	def add(self, name):
		if name.get().find(' ') != -1: return
		self.attributes[name.get()] = False
		self.attributes_widgets()

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
			self.rects[tuple(tile_pos)] = self.attributes.copy()
		self.refresh()

	def remove_tile(self, event):
		tile_pos = self.get_tile_pos(event.x, event.y)
		if tuple(tile_pos) in self.rects:
			self.rects.pop(tuple(tile_pos))
		self.refresh()


if __name__ == '__main__':
	Editor()
