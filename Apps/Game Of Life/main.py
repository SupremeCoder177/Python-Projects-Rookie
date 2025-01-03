# Game Of Life 

import customtkinter as ctk
import threading
from random import randint

APP_SIZE = (850, 600)
TILE_SIZE = 25

class App(ctk.CTk):

	def __init__(self):
		super().__init__()
		ctk.set_appearance_mode('dark')
		self.title("Game Of Life")
		self.resizable(False, False)

		x = (self.winfo_screenwidth() - APP_SIZE[0]) // 2
		y = (self.winfo_screenheight() - APP_SIZE[1]) // 2

		self.geometry(f'{APP_SIZE[0]}x{APP_SIZE[1]}+{x}+{y}')
		self.rects = {}
		self.add_rects(0)
		self.add_widgets()

		self.bind("<Escape>", lambda event: self.quit())
		self.stop_event = threading.Event()
		self.mainloop()

	def add_rects(self, pattern):
		for x in range(APP_SIZE[0] // TILE_SIZE):
			for y in range(APP_SIZE[1] // TILE_SIZE):
				if pattern == 0:
					self.rects[(x, y)] = False
				if pattern == 1:
					self.rects[(x, y)] = bool(randint(0, 1))	

	def add_widgets(self):
		self.rowconfigure(0, weight = 1, uniform = 'a')
		self.columnconfigure(0, weight = 3, uniform = 'a')
		self.columnconfigure(1, weight = 1, uniform = 'a')

		font = ctk.CTkFont(family = 'Cascadia Mono', size = 15)

		self.canvas = ctk.CTkCanvas(self, bg = 'black')
		self.canvas.grid(row = 0, column = 0, sticky = 'NSEW')

		frame = ctk.CTkFrame(self, fg_color = 'transparent')

		self.start_btn = ctk.CTkButton(frame, text = "Start",
			font = font,
			command = self.start)
		self.start_btn.pack(expand = True, pady = 10)

		self.stop_btn = ctk.CTkButton(frame, text = "Stop",
			font = font,
			command = self.stop)
		self.stop_btn.pack(expand = True, pady = 10)

		self.rand_btn = ctk.CTkButton(frame,
			text = 'Set Random',
			font = font,
			command = self.set_random)
		self.rand_btn.pack(expand = True, pady = 10)

		self.delete_btn = ctk.CTkButton(frame,
			text = "Delete All",
			font = font,
			command = self.delete)
		self.delete_btn.pack(expand = True, pady = 10)

		frame.grid(row = 0, column = 1, sticky = 'NSEW')
		self.canvas.bind('<Button-1>', self.add_tile)
		self.canvas.bind('<Button-3>', self.remove_tile)
		self.place_tiles()

	def set_random(self):
		self.add_rects(1)
		self.refresh()

	def delete(self):
		self.add_rects(0)
		self.refresh()

	def start(self):
		self.stop_event.clear()
		self.loop = threading.Thread(target = self.play_gen)
		self.loop.daemon = True

		self.stop_btn.configure(state = 'normal')
		self.start_btn.configure(state = 'disabled')
		self.rand_btn.configure(state = 'disabled')
		self.delete_btn.configure(state = 'disabled')
		self.canvas.unbind('<Button-1>')
		self.canvas.unbind('<Button-3>')
		self.loop.start()

	def stop(self):
		self.stop_event.set()
		self.start_btn.configure(state = 'normal')
		self.stop_btn.configure(state = 'disabled')
		self.rand_btn.configure(state = 'normal')
		self.delete_btn.configure(state = 'normal')
		self.canvas.bind('<Button-1>', self.add_tile)
		self.canvas.bind('<Button-3>', self.remove_tile)

	def get_pos(self, pos):
		return (int(pos[0] // TILE_SIZE), int(pos[1] // TILE_SIZE))

	def get_neighbours(self, rect):
		NEIGHBOUR_OFFSETS = [(-1, -1),
		(0, -1), (1, -1),
		(-1, 0), (1, 0),
		(-1, 1), (0, 1), (1, 1)]
		temp = []
		for offset in NEIGHBOUR_OFFSETS:
			temp.append((rect[0] + offset[0], rect[1] + offset[1]))
		temp = [rect for rect in temp if rect in self.rects]
		return temp

	def get_next_gen(self):
		for rect in self.rects:
			live_count = 0
			neighbours = self.get_neighbours(rect)
			for neighbour in neighbours:
				if self.rects[neighbour]: live_count += 1
			if live_count < 2:
				if self.rects[rect]: self.rects[rect] = False
			if live_count == 3:
				if not self.rects[rect]: self.rects[rect] = True
				if self.rects[rect]: pass
			if live_count == 2:
				if self.rects[rect]: pass
			if live_count > 3:	
				if self.rects[rect]: self.rects[rect] = False

	def play_gen(self):
		while not self.stop_event.is_set():
			self.get_next_gen()
			self.refresh()
			self.stop_event.wait(0.1)

	def add_tile(self, event):
		pos = self.get_pos((event.x, event.y))
		if pos not in list(self.rects.keys()): return
		if not self.rects[pos]:
			self.rects[pos] = True
		self.refresh()

	def remove_tile(self, event):
		pos = self.get_pos((event.x, event.y))
		if pos not in self.rects.keys(): return
		if self.rects[pos]:
			self.rects[pos] = False
		self.refresh()

	def place_tiles(self):
		for rect in self.rects:
			if self.rects[rect]:
				x = rect[0] * TILE_SIZE
				y = rect[1] * TILE_SIZE
				self.canvas.create_rectangle(x, y, x + TILE_SIZE, y + TILE_SIZE, fill = 'white')

	def refresh(self):
		self.canvas.delete('all')
		self.place_tiles()


if __name__ == '__main__':
	App()