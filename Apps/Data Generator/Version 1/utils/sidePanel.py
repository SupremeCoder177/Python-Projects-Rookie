# this module defiend the GUI for the side panel

import customtkinter as ctk
from utils.animations import Animations
from utils.generator import DATA_TYPES
from utils.commonWidgets import LabelEntry, LabelOptions


# this class defines the GUI for the side panel inputs
class InputFrame(ctk.CTkFrame):

	def __init__(self, master : ctk.CTkFrame, settings : dict):
		pass


class SidePanel(ctk.CTkFrame):

	def __init__(self, master : ctk.CTk, settings : dict, console):
		super().__init__(master = master, corner_radius = 0)

		# variables
		self.settings = settings
		self.console = console
		self.start_x = self.settings["side_panel_start_pos"][0]
		self.end_x = self.settings["side_panel_shown_pos"][0]
		self.y = self.settings["side_panel_start_pos"][1]
		self.hidden = True
		self.anim_time = 150 # milliseconds

		self.name = ctk.StringVar()
		self.d_type = ctk.StringVar()
		self.lower = ctk.StringVar()
		self.upper = ctk.StringVar()

		# adding the widgets

		# the input widgets container
		inputs_container = ctk.CTkFrame(self)
		inputs_container.place(relx = 0.02, rely = 0.02, relwidth = 0.96, relheight = 0.8)

		inputs_container.rowconfigure((0, 1), weight = 1, uniform = 'a')
		inputs_container.columnconfigure((0, 1), weight = 1, uniform = 'a')

		frame1 = LabelEntry(inputs_container, self.name, "Column\nName")
		frame2 = LabelOptions(inputs_container, DATA_TYPES, self.d_type, "Data\nType")
		frame3 = LabelEntry(inputs_container, self.lower, "Lower")
		frame4 = LabelEntry(inputs_container, self.upper, "Upper")

		# adding the sub-sub-frames
		frame1.grid(row = 0, column = 0, sticky = "NSEW")
		frame2.grid(row = 0, column = 1, sticky = "NSEW")
		frame3.grid(row = 1, column = 0, sticky = "NSEW")
		frame4.grid(row = 1, column = 1, sticky = "NSEW")


		# the button to add the column to the main panel
		ctk.CTkButton(self,
			text = "Add Column Heading",
			command = self.master.add_column_to_main).place(relx = 0.2, rely = 0.84, relwidth = 0.6, relheight = 0.12)

		self.place(relx = self.start_x, rely = self.y, relwidth = self.settings["side_panel_dimensions"][0], relheight = self.settings["side_panel_dimensions"][1])

	# this function moves the panel from hidden to shown, or shown to hidden
	def move(self) -> None:
		if self.hidden:
			Animations().slide_frame_horizontal(self, self.start_x, self.end_x, self.y, self.anim_time)
		else:
			Animations().slide_frame_horizontal(self, self.end_x, self.start_x, self.y, self.anim_time)
		self.hidden = not self.hidden

	# returns true if not hidden, else false
	def is_shown(self) -> bool:
		return not self.hidden

	# returns the data in the variables, self.lower, self.upper, self.name and self.d_type in the
	# form of a HashMap
	def get_data(self) -> dict:
		
		# checking if the self.lower and self.upper values are integers
		lower = 0
		upper = 0
		try:
			lower = int(self.lower.get())
			upper = int(self.upper.get())
		except ValueError as e:
			self.console.display_error()
			return {}
		if lower < upper:
			return {"name" : self.name.get(), "type" : self.d_type.get(), "lower" : lower, "upper" : upper}
		else:
			return {}

