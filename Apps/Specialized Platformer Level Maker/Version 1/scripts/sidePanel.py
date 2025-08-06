# Side Panel GUI implementation


import customtkinter as ctk
from collections.abc import Callable
from . import animations as anims
from PIL import Image

# some global variables for storing images and stuff

toggle_image = ctk.CTkImage(
	light_image = Image.open("Images/toggle_btn_dark.png"),
	dark_image = Image.open("Images/toggle_btn_light.png"),
	size = (40, 40))

light_image = Image.open("Images/theme_mode_light.png")
resized = light_image.resize((150, 150))

theme_image = ctk.CTkImage(
	light_image = resized,
	dark_image = Image.open("Images/theme_mode_dark.png"),
	size = (150, 150))

class SidePanel:

	# reset is for resetting the panel theme
	def __init__(self, panel : ctk.CTkFrame, reset : Callable, settings : dict):
		if not isinstance(reset, Callable):
			raise ValueError("reset argument not a function")
		self.panel = panel
		self.reset = reset
		self.settings = settings
		self.controls_shown = False

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

		# second a button to toggle between theme modes
		ctk.CTkButton(self.panel,
			text = "",
			image = theme_image,
			fg_color = "transparent").grid(row = 0, column = 1, sticky = "NS")



	def show_controls(self):
		panel = self.panel.master.control_panel
		_from = (self.settings["control_panel_x"], self.settings["control_panel_y"]) if not self.controls_shown else (self.settings["control_panel_shown_x"], self.settings["control_panel_shown_y"])
		to = (self.settings["control_panel_x"], self.settings["control_panel_y"]) if self.controls_shown else (self.settings["control_panel_shown_x"], self.settings["control_panel_shown_y"])
		time = 400 # milliseconds
		anims.move_frame(_from, to, time, panel)
		self.controls_shown = not self.controls_shown
