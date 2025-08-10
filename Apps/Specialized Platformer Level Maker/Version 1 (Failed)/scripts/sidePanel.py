# Side Panel GUI implementation


import customtkinter as ctk
from . import animations as anims
from tkinter import filedialog
from PIL import Image

# some global variables for storing images and stuff

toggle_image = ctk.CTkImage(
	light_image = Image.open("Images/toggle_btn_dark.png"),
	dark_image = Image.open("Images/toggle_btn_light.png"),
	size = (40, 40))

class SidePanel:

	# reset is for resetting the panel theme
	def __init__(self, panel : ctk.CTkFrame, settings : dict):
		self.panel = panel
		self.settings = settings
		self.controls_shown = False

		self.max_cols = 3
		self.panel_cell_size = (settings["app_size"][0] * settings["side_panel_width"]) // self.max_cols
		self.cell_size = 10
		self.slide_var = ctk.IntVar(value = 10)
		self.y_padding = 20
		self.x_padding = 20
		self.added = set()

		# adding the GUI layout
		self.panel.columnconfigure((0, 1), weight = 1, uniform = 'a')
		self.panel.rowconfigure(0, weight = 1, uniform = 'a')
		self.panel.rowconfigure(1, weight = 6, uniform = 'a')
		self.panel.rowconfigure(2, weight = 2, uniform = 'a')

		# first a button to toggle the control panel
		ctk.CTkButton(self.panel,
			text = "",
			image = toggle_image,
			fg_color = settings["toggle_btn_color"],
			hover_color = settings["toggle_btn_hover_color"],
			command = self.show_controls).grid(row = 0, column = 0, sticky = "NS")

		# second a switch to toggle between theme modes
		ctk.CTkSwitch(self.panel,
			text = "Change Theme",
			progress_color = settings["theme_switch_color"],
			font = ctk.CTkFont(family = settings["font"], size = 12),
			width = 40,
			height = 20,
			command = panel.master.change_theme).grid(row = 0, column = 1, sticky = "NS")

		# the frame to hold the loaded sprites and selection
		self.sprites_frame = ctk.CTkScrollableFrame(self.panel, fg_color = settings["sprites_frame_color"])

		self.sprites_frame.grid(row = 1, column = 0, columnspan = 2, sticky="NSEW", pady = 10)

		# the frame for the buttons to load and unload sprites
		self.sprites_loader_frame = ctk.CTkFrame(self.panel, fg_color = settings["sprites_loader_color"])

		# adding the load button
		ctk.CTkButton(self.sprites_loader_frame,
			text = "Load Image",
			font = ctk.CTkFont(family = settings["font"], size = 20),
			command = self.get_path,
			fg_color = settings["normal_btn_color"],
			hover_color = settings["normal_btn_hover_color"],
			text_color = settings["normal_btn_text_color"]).pack(pady = 10)

		ctk.CTkButton(self.sprites_loader_frame,
			text = "Delete Sprite",
			font = ctk.CTkFont(family = settings["font"], size = 20),
			command = self.panel.master.del_sprite,
			fg_color = settings["normal_btn_color"],
			hover_color = settings["normal_btn_hover_color"],
			text_color = settings["normal_btn_text_color"]).pack(pady = 5)

		ctk.CTkButton(self.sprites_loader_frame,
			text = "Delete All",
			font = ctk.CTkFont(family = settings["font"], size = 20),
			command = self.panel.master.del_sprites,
			fg_color = settings["normal_btn_color"],
			hover_color = settings["normal_btn_hover_color"],
			text_color = settings["normal_btn_text_color"]).pack(pady = 5)

		ctk.CTkSlider(self.sprites_loader_frame,
			from_ = 10,
			to = 200,
			variable = self.slide_var,
			command = self.change_cell_size,
			button_color = settings["slider_color"],
			button_hover_color = settings["slider_hover_color"]).pack(pady = 5)

		self.label = ctk.CTkLabel(self.sprites_loader_frame,
			text = f'Cell Size : {self.slide_var.get()}',
			font = ctk.CTkFont(family = settings["font"], size = 20),
			fg_color = "transparent")
		self.label.pack(pady = 10)

		self.sprites_loader_frame.grid(row = 2, column = 0, columnspan = 2, sticky = "NSEW")

	def show_controls(self):
		panel = self.panel.master.control_panel
		_from = (self.settings["control_panel_x"], self.settings["control_panel_y"]) if not self.controls_shown else (self.settings["control_panel_shown_x"], self.settings["control_panel_shown_y"])
		to = (self.settings["control_panel_x"], self.settings["control_panel_y"]) if self.controls_shown else (self.settings["control_panel_shown_x"], self.settings["control_panel_shown_y"])
		time = 200 # milliseconds
		anims.move_frame(_from, to, time, panel)
		self.controls_shown = not self.controls_shown

	def get_path(self):
		path = filedialog.askopenfile()
		if path and path.name.endswith(".png"):
			self.add_sprites(path)

	def add_sprites(self, path):
		try:
			img = Image.open(path.name)	
			size = img.size
			for i in range(size[0] // self.cell_size):
				for j in range(size[1] // self.cell_size):
					temp = img.crop((i * self.cell_size, j * self.cell_size, (i + 1) * self.cell_size, (j + 1) * self.cell_size))
					ctk_img = ctk.CTkImage(light_image = temp, dark_image = temp, size = (self.panel_cell_size, self.panel_cell_size))
					self.panel.master.sprites[self.panel.master.num_sprites + 1] = {
					"path" : path.name,
					"position" : [i, j],
					"cell_size" : self.cell_size,
					"img" : ctk_img,
					"img_dimen" : temp.size
					}
					self.panel.master.num_sprites += 1
		except Exception as e:
			print(e)
		self.add_sprites_to_panel()

	def add_sprites_to_panel(self):
		row = col = 0
		for index, info in self.panel.master.sprites.items():
			if index in self.added:
				continue
			else:
				self.added.add(index)
				ctk.CTkButton(self.sprites_frame,
					text="",
					image = info["img"],
					width = self.panel_cell_size, height = self.panel_cell_size,
					command = lambda ind=index: self.panel.master.set_sprite(ind)).grid(row = row, column = col)
				col += 1
				if col >= self.max_cols:
					col = 0
					row += 1

	def re_render_sprites(self):
		for child in self.sprites_frame.winfo_children():
			child.destroy()
		self.added = set()
		self.x = self.y = 0
		self.add_sprites_to_panel()

	def change_cell_size(self, var):
		self.cell_size = round(var)
		self.label.configure(text = f'Cell Size : {round(var)}')



