# this module defiend the GUI for the side panel

import customtkinter as ctk
from utils.animations import Animations


class SidePanel(ctk.CTkFrame):

	def __init__(self, master : ctk.CTk, settings : dict):
		super().__init__(master = master, corner_radius = 0)
		self.settings = settings

		# variables
		self.start_x = self.settings["side_panel_start_pos"][0]
		self.end_x = self.settings["side_panel_shown_pos"][0]
		self.y = self.settings["side_panel_start_pos"][1]
		self.hidden = True
		self.anim_time = 500 # milliseconds

		# adding the widgets

		# the input widgets container
		self.inputs_container = ctk.CTkFrame(self)
		self.inputs_container.place(relx = 0.02, rely = 0.02, relwidth = 0.96, relheight = 0.8)


		self.place(relx = self.start_x, rely = self.y, relwidth = self.settings["side_panel_dimensions"][0], relheight = self.settings["side_panel_dimensions"][1])

	# this function moves the panel from hidden to shown, or shown to hidden
	def move(self) -> None:
		if self.hidden:
			Animations().slide_frame_horizontal(self, self.start_x, self.end_x, self.y, self.anim_time)
		else:
			Animations().slide_frame_horizontal(self, self.end_x, self.start_x, self.y, self.anim_time)
		self.hidden = not self.hidden
