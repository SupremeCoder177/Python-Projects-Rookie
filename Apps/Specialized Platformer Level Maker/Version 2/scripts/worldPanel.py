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
		self.items = dict()
		self.placed = dict()
		self.count = 0

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
		self.master.builder.add_cell((self.grid_pos_x, self.grid_pos_y))
		img = ImageTk.PhotoImage(self.master.handler.sprites[self.master.handler.curr_sprite]["sprite"])
		x = self.grid_pos_x * self.tile_size + (self.tile_size / 2) - self.offset_x
		y = self.grid_pos_y * self.tile_size + (self.tile_size / 2) - self.offset_y
		img_id = self.create_image(x, y, image=img)
		if (self.grid_pos_x, self.grid_pos_y) not in self.placed:
			self.placed[(self.grid_pos_x, self.grid_pos_y)] = {"stack_level" : 1, "counts" : [self.count]}
		else:
			self.placed[(self.grid_pos_x, self.grid_pos_y)]["stack_level"] += 1
			self.placed[(self.grid_pos_x, self.grid_pos_y)]["counts"].append(self.count)
		self.items[self.count] = {
		"img" : img,
		"id" : img_id,
		"pos" : tuple(self.get_grid_pos()),
		"level" : self.placed[tuple(self.get_grid_pos())]["stack_level"]
		}
		self.count += 1

	def erase(self):
		if tuple(self.get_grid_pos()) in self.placed:
			for count in self.placed[tuple(self.get_grid_pos())]["counts"]:
				if self.items[count]["level"] == self.placed[tuple(self.get_grid_pos())]["stack_level"]:
					del self.items[count]
					self.master.builder.delete_cell(tuple(self.get_grid_pos()))
					self.placed[tuple(self.get_grid_pos())]["stack_level"] -= 1
					if self.placed[tuple(self.get_grid_pos())]["stack_level"] >= 1:
						self.placed[tuple(self.get_grid_pos())]["counts"].pop()
					else:
						del self.placed[tuple(self.get_grid_pos())]
		else:
			self.master.show_err("Nothing to erase !")

	def change_offset(self, dx, dy):
		self.move("all", dx, dy)
		self.offset_x -= dx
		self.offset_y -= dy
		self.change_pos(self.x, self.y)
		
	def clear(self):
		self.items = dict()
		self.placed = dict()
		self.x = self.y = self.offset_y = self.offset_x = self.count = 0
		self.master.control.update_mouse_info()