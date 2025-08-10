# this module defines the GUI for the side panel

import customtkinter as ctk
from scripts.animations import move_frame
from PIL import Image

# settings the img size to show on buttons
img_size = (50, 50)

# loading images to display on buttons
control_btn_image = ctk.CTkImage(
	light_image = Image.open("Images/toggle_btn_dark.png"),
	dark_image = Image.open("Images/toggle_btn_light.png"),
	size = img_size)

theme_btn_image = ctk.CTkImage(
	light_image = Image.open("Images/theme_mode_light.png"),
	dark_image = Image.open("Images/theme_mode_dark.png"),
	size = img_size)

load_btn_image = ctk.CTkImage(
	light_image = Image.open("Images/open_image_light.png"),
	dark_image = Image.open("Images/open_image_dark.png"),
	size = img_size)


# this frame lists all the controls the app has, i.e. the keyboard bindings, because doing everything with your
# mouse is kind of slow
class Controls(ctk.CTkFrame):

	def __init__(self, master):
		super().__init__(master = master)
		settings = master.settings
		self.shown_pos = settings["controls_show_panel_show_pos"]
		self.hidden_pos = settings["controls_show_panel_pos"]
		self.shown = False

		self.place(relx = settings["controls_show_panel_pos"][0], rely = settings["controls_show_panel_pos"][1], relwidth = settings["controls_show_panel_size"][0], relheight = settings["controls_show_panel_size"][1])

	def toggle_show_self(self):
		if not self.shown:
			move_frame(self, 300, self.hidden_pos, self.shown_pos, None)
		else:
			move_frame(self, 300, self.shown_pos, self.hidden_pos, None)
		self.shown = not self.shown


# main panel
class SidePanel(ctk.CTkFrame):

	def __init__(self, master):
		super().__init__(master = master)
		self.settings = master.settings

		# setting some constants
		self.max_cols = 2

		# designing the layout
		self.columnconfigure((0, 1), weight = 1, uniform = 'a')
		self.rowconfigure(0, weight = 1, uniform = 'a')
		self.rowconfigure(1, weight = 4, uniform = 'a')
		self.rowconfigure(2, weight = 1, uniform = 'a')
		self.rowconfigure(3, weight = 1, uniform = 'a')

		# adding the widgets

		# the control panel toggle button
		ctk.CTkButton(self,
			text="",
			image = control_btn_image,
			fg_color = self.settings["btn_color"],
			hover_color = self.settings["btn_hover_color"],
			width = self.settings["btn_size"][0],
			height = self.settings["btn_size"][1],
			command = master.toggle_control).grid(row = 0, column = 0, sticky = "NW")

		# the theme toggle button
		ctk.CTkButton(self,
			text="",
			image = theme_btn_image,
			fg_color = self.settings["btn_color"],
			hover_color = self.settings["btn_hover_color"],
			width = self.settings["btn_size"][0],
			height = self.settings["btn_size"][1],
			command = master.change_theme).grid(row = 0, column = 1, sticky = "NE")

		# scrollable frame to display all the loaded sprites
		self.sprites_frame = ctk.CTkScrollableFrame(self)
		self.sprites_frame.grid(row = 1, column = 0, columnspan = 2, sticky = "NSEW")

		# button to load sprites from an image
		ctk.CTkButton(self,
			text="",
			image = load_btn_image,
			fg_color = self.settings["btn_color"],
			hover_color = self.settings["btn_hover_color"],
			width = self.settings["btn_size"][0],
			height = self.settings["btn_size"][1],
			command = master.load_sprites).grid(row = 2, column = 0, sticky = "SW")

		# button to unload current selected sprite
		ctk.CTkButton(self,
			text = "D",
			fg_color = self.settings["btn_color"],
			hover_color = self.settings["btn_hover_color"],
			width = self.settings["btn_size"][0],
			height = self.settings["btn_size"][1],
			font = ctk.CTkFont(family = self.settings["font"], size = 50),
			text_color = self.settings["btn_txt_color"],
			command = master.delete_sprite).grid(row = 2, column = 1, sticky = "SE")

		# button to unload all sprites
		ctk.CTkButton(self,
			text = "DA",
			fg_color = self.settings["btn_color"],
			hover_color = self.settings["btn_hover_color"],
			width = self.settings["btn_size"][0],
			height = self.settings["btn_size"][1],
			font = ctk.CTkFont(family = self.settings["font"], size = 50),
			text_color = self.settings["btn_txt_color"],
			command = master.delete_all).grid(row = 3, column = 0, sticky = "SW")

		# creating a frame which shows all keyboard bindings
		self.controls = Controls(self.master)

		# button to show controls
		ctk.CTkButton(self,
			text = "C",
			fg_color = self.settings["btn_color"],
			hover_color = self.settings["btn_hover_color"],
			width = self.settings["btn_size"][0],
			height = self.settings["btn_size"][1],
			font = ctk.CTkFont(family = self.settings["font"], size = 50),
			text_color = self.settings["btn_txt_color"],
			command = self.controls.toggle_show_self).grid(row = 3, column = 1, sticky = "SE")

		# placing panel on screen
		self.place(relx = self.settings["side_panel_pos"][0], rely = self.settings["side_panel_pos"][1], relwidth = self.settings["side_panel_size"][0], relheight = self.settings["side_panel_size"][1])
		self.lift(aboveThis = self.controls)

	# displays the sprites passed in on the frame as images on buttons
	def display_sprites(self, sprites):
		row = 0
		col = 0
		for tag, info in sprites.items():
			temp = ctk.CTkImage(light_image = info["sprite"],
				dark_image = info["sprite"],
				size = self.settings["sprite_display_cell_size"])
			ctk.CTkButton(self.sprites_frame,
				text="",
				image = temp,
				fg_color = self.settings["sprite_display_color"],
				hover_color = self.settings["sprite_display_hover_color"],
				command = lambda tag=tag: self.master.change_curr_sprite(tag)).grid(row = row, column = col, sticky = "NSEW")
			col += 1
			if col >= self.max_cols:
				col = 0
				row += 1

	# deletes all displayed sprites on the sprite_frame and then re-render the updates sprites list passed in
	def update(self, sprites):
		for child in self.sprites_frame.winfo_children():
			child.destroy()
		self.display_sprites(sprites)
