# main

import customtkinter as ctk
from widgets import *
from settings import *
import os
import json

class App(ctk.CTk):

	def __init__(self):
		super().__init__()
		ctk.set_appearance_mode('dark')
		self.title("Editor")

		x = (self.winfo_screenwidth() -  SCREEN_SIZE[0]) // 2
		y = (self.winfo_screenheight() -  SCREEN_SIZE[1]) // 2

		self.geometry(f'{SCREEN_SIZE[0]}x{SCREEN_SIZE[1]}+{x}+{y}')
		self.resizable(False, False)

		self.path = ctk.StringVar(value = 'Enter Path Here')
		self.lvl = ctk.StringVar()
		self.font = ctk.CTkFont(family = FONT, size = FONT_SIZE)
		self.map = {}
		self.rects = {}
		self.tile_size = TILE_SIZE
		self.offset = [0, 0]
		self.attributes = {'color' : 'gray', 'physics' : True}

		self.input = Input(self, self.path, self.lvl, self.font)

		self.bind('<Escape>', lambda event: self.quit())
		self.mainloop()

	def load_map(self):
		if not os.path.exists(self.path.get()): return
		if not self.lvl.get(): return

		if os.path.exists(os.path.join(self.path.get(), f'{self.lvl.get()}.json')):
			with open(f'{self.path.get()}/{self.lvl.get()}.json', 'r')  as file:
				self.map = json.load(file)
			if not file.closed: file.close()
		else:
			with open(f'{self.path.get()}/{self.lvl.get()}.json', 'w') as file:
				json.dump({}, file)
			if not file.closed: file.close()

		self.input.pack_forget()
		self.convert()

	def convert(self):
		if not self.map: return

		for tile in self.map:
			temp = tuple(map(int, tile.split(';')))
			self.rects[temp] = self.map[tile]
		self.attributes = list(self.rects.values())[0].copy()
		self.editor = EditorWidgets(self)
		self.bind('<KeyPress>', self.editor.change_offset)
		self.bind('<MouseWheel>', self.editor.zoom)
		self.editor.pack(expand = True, fill = 'both')
		self.editor.refresh()

	def save(self):
		self.map.clear()
		for rect in self.rects:
			temp = ';'.join(map(str, rect))
			self.map[temp] = self.rects[rect]
		with open(f'{self.path.get()}/{self.lvl.get()}.json', 'w') as file:
			json.dump(self.map, file, sort_keys = True, indent = 4)
		if not file.closed: file.close()

	def reset(self):
		self.map = {}
		self.rects = {}
		self.attributes = {'color' : 'gray', 'physics' : True}
		self.tile_size = TILE_SIZE 
		self.offset = [0, 0]
		self.editor.pack_forget()
		self.input.pack(expand = True, fill = 'both')


if __name__ == '__main__':
	App()