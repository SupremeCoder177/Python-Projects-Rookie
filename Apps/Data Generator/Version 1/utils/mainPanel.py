# this module handles all the widgets in the main panel

import customtkinter as ctk
from typing import List


# this class defines the columns stored in the column container widget of the main panel (see below)
class Column(ctk.CTkFrame):

	def __init__(self):
		pass


# the main panel
class MainPanel(ctk.CTkFrame):

	def __init__(self, master : ctk.CTk, settings : dict):
		super().__init__(master = master)
		self.settings = settings

		# adding the main panel widgets

		# main label
		ctk.CTkLabel(self, text = "Columns in current CSV File").place(relx = 0.2, rely = 0.01, relwidth = 0.6, relheight = 0.1)

		# column container
		self.column_container = ctk.CTkScrollableFrame(self)
		self.column_container.place(relx = 0.01, rely = 0.12, relwidth = 0.98, relheight = 0.75)

		# frame to hold all the buttons
		self.buttons_container = ctk.CTkFrame(self,
			fg_color = self.settings["main_panel_btn_container_bg"],
			border_color = self.settings["main_panel_btn_container_border_color"])
		self.buttons_container.place(relx = 0.01, rely = 0.89, relwidth = 0.98, relheight = 0.1)

		# adding a grid to the buttons container
		self.buttons_container.columnconfigure((0, 1, 2), weight = 1, uniform = 'a')
		self.buttons_container.rowconfigure((0, 1), weight = 1, uniform = 'a')

		# adding the buttons

		# the button which shows/hides the side panel
		ctk.CTkButton(self.buttons_container,
			text = "Add",
			command = self.master.side_panel.move).grid(row = 1, column = 0, sticky = "NSEW")

		# the button which deletes the selected columns


		# the button which generates the data


		# the button which saves the data into a csv 


		self.place(relx = self.settings["main_panel_pos"][0], rely = self.settings["main_panel_pos"][1], relwidth = self.settings["main_panel_dimensions"][0], relheight = self.settings["main_panel_dimensions"][1])

	# adds a column to the GUI column container
	def add_column(self) -> None:
		pass

	# deletes all the columns from the column container
	def reset_columns(self) -> None:
		pass

	# deletes a specific column/columns from the column container
	def delete_column(self, index : int | List[int]) -> None:
		pass