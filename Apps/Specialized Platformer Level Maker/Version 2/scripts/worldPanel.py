# this module defines the GUI for the worldPanel, which is where the user will build their levels

import customtkinter as ctk
from PIL import ImageTk

class WorldPanel(ctk.CTkCanvas):

	def __init__(self, master):
		super().__init__(master = master)
		self.settings = master.settings
		self.change_bg()

		# variables
		self.x = self.y = 0
		self.offset_x = self.offset_y = 0
		self.grid_pos_x = self.grid_pos_y = 0
		self.tile_size = self.settings["world_grid_size"]
		self.occupied = dict()

		self.place(relx = self.settings["world_panel_pos"][0], rely = self.settings["world_panel_pos"][1], relwidth = self.settings["world_panel_size"][0], relheight = self.settings["world_panel_size"][1])
		self.bind("<Motion>", lambda event: self.change_pos(event.x, event.y))
		self.bind("<Button-1>", lambda event: self.draw())
		self.bind("<Button-3>", lambda event: self.erase())

	# since there is no in-built dark and light mode for canvas, this is an implementation of my own
	def change_bg(self):
		self.bg = self.settings["world_color"][0] if self.master.theme == "light" else self.settings["world_color"][1]
		self.configure(bg = self.bg)

	def change_pos(self, x, y):
		self.x = x + self.offset_x
		self.y = y + self.offset_y
		self.grid_pos_x = self.x // self.tile_size
		self.grid_pos_y = self.y // self.tile_size
		self.master.control.update_mouse_info()

	def get_grid_pos(self):
		return self.grid_pos_x, self.grid_pos_y

	def get_world_pos(self):
		return self.x, self.y

	def draw(self):
		if not self.master.handler.curr_sprite: return
		if (self.grid_pos_x, self.grid_pos_y) not in self.occupied:
			self.master.builder.add_cell((self.grid_pos_x, self.grid_pos_y))
			img = ImageTk.PhotoImage(self.master.handler.sprites[self.master.handler.curr_sprite]["sprite"])
			x = self.grid_pos_x * self.tile_size + (self.tile_size / 2)
			y = self.grid_pos_y * self.tile_size + (self.tile_size / 2)
			img_id = self.create_image(x, y, image=img)
			self.occupied[(self.grid_pos_x, self.grid_pos_y)] = img, img_id
		else:
			self.master.show_err("Cell already occupied !")

	def erase(self):
		if tuple(self.get_grid_pos()) in self.occupied:
			del self.occupied[tuple(self.get_grid_pos())]
			self.master.builder.delete_cell(tuple(self.get_grid_pos()))
		else:
			self.master.show_err("Nothing to erase !")

	def change_offset(self, dx, dy):
		self.move("all", dx, dy)
		self.offset_x -= dx
		self.offset_y -= dy
		self.change_pos(self.x, self.y)
		