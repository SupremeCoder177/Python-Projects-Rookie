# this module handles all the widgets in the main panel

import customtkinter as ctk
from typing import List
from utils.commonWidgets import LabelEntry, LabelOptions
from utils.generator import DATA_TYPES


# this class defines the columns stored in the column container widget of the main panel (see below)
class ColumnHeading(ctk.CTkFrame):

	def __init__(self, master : ctk.CTkFrame, settings : dict, column_name : str, column_data_type : str, lower_range : int, upper_range : int, index : int, master_of_master : ctk.CTkFrame):
		# initializing the color theme
		super().__init__(master = master, fg_color = settings["column_heading_fg_color"],
			border_color = settings["column_heading_border_color"])
		self.pack_propagate(False)

		# variables
		self.settings = settings
		self.master_of_master = master_of_master
		self.name = ctk.StringVar(value = column_name)
		self.d_type = ctk.StringVar(value = column_data_type)
		self.lower = ctk.StringVar(value = lower_range)
		self.upper = ctk.StringVar(value = upper_range)
		self.selected = False
		self.permanent_select = False
		self.edit_mode = False

		# adding the widgets

		# the index label
		self.index_label = ctk.CTkLabel(self,
			text = index)
		self.index_label.place(relx = 0.01, rely = 0.01, relwidth = 0.15, relheight = 0.15)

		# the edit button
		ctk.CTkButton(self,
			text = "Edit",
			command = self.toggle_state).place(relx = 0.01, rely = 0.84, relwidth = 0.2, relheight = 0.15)

		# the save changes button
		self.save_btn = ctk.CTkButton(self,
			text = "Save Changes",
			state = "disabled")
		self.save_btn.place(relx = 0.54, rely = 0.84, relwidth = 0.25, relheight = 0.15)

		# the ignore changes button
		self.cancel_btn = ctk.CTkButton(self,
			text = "Cancel",
			state = "disabled",
			command = self.toggle_state)
		self.cancel_btn.place(relx = 0.79, rely = 0.84, relwidth = 0.2, relheight = 0.15)

		# sub-frames
		self.name_frame = LabelEntry(self, self.name, "Name")
		self.type_frame = LabelOptions(self, DATA_TYPES, self.d_type, "Type")
		self.lower_frame = LabelEntry(self, self.lower, "Lower")
		self.upper_frame = LabelEntry(self, self.upper, "Upper")

		# placing the sub-frames
		self.name_frame.place(relx = 0.2, rely = 0.01, relwidth = 0.3, relheight = 0.4)
		self.type_frame.place(relx = 0.5, rely = 0.01, relwidth = 0.3, relheight = 0.4)
		self.lower_frame.place(relx = 0.2, rely = 0.41, relwidth = 0.3, relheight = 0.4)
		self.upper_frame.place(relx = 0.5, rely = 0.41, relwidth = 0.3, relheight = 0.4)

		# disabling the inputs for the sub-frames
		self.name_frame.entry.configure(state = "disabled")
		self.type_frame.menu.configure(state = "disabled")
		self.lower_frame.entry.configure(state = "disabled")
		self.upper_frame.entry.configure(state = "disabled")

		# event bindings
		self.bind("<Enter>", lambda event: self.selection_status_toggle())
		self.bind("<Leave>", lambda event: self.selection_status_toggle())
		self.bind("<Button-1>", self.toggle_perma_select)
		self.bind("<Button-1>", self.master_of_master.focus_panel)

		self.pack(pady = 10, padx = 10, fill = 'x')

	# changes the selection status of the frame
	def selection_status_toggle(self) -> None:
		self.selected = not self.selected
		self.change_color()

	# enables/disables the edit inputs and buttons
	def toggle_state(self):
		self.edit_mode = not self.edit_mode

		if self.edit_mode:
			self.save_btn.configure(state = "normal")
			self.cancel_btn.configure(state = "normal")
			self.name_frame.entry.configure(state = "normal")
			self.type_frame.menu.configure(state = "normal")
			self.lower_frame.entry.configure(state = "normal")
			self.upper_frame.entry.configure(state = "normal")
		else:
			self.save_btn.configure(state = "disabled")
			self.cancel_btn.configure(state = "disabled")
			self.name_frame.entry.configure(state = "disabled")
			self.type_frame.menu.configure(state = "disabled")
			self.lower_frame.entry.configure(state = "disabled")
			self.upper_frame.entry.configure(state = "disabled")

	# toggle the permanent select variable
	def toggle_perma_select(self, event):
		self.permanent_select = not self.permanent_select

	# changes the fg_color if the mouse enters or leaves the frame
	def change_color(self) -> None:
		self.configure(fg_color = self.settings["column_heading_fg_color_selected"] if self.selected or self.permanent_select else self.settings["column_heading_fg_color"])

	# changes the index label text
	def change_index(self, index) -> None:
		self.index_label.configure(text = index)

	# returns the name of the column
	def get_name(self) -> str:
		return self.name.get()

	# tries to change the data with the
	# new input data
	def change_data(self):
		pass


# the main panel
class MainPanel(ctk.CTkFrame):

	def __init__(self, master : ctk.CTk, settings : dict, console):
		super().__init__(master = master)

		# variables
		self.settings = settings
		self.console = console
		self.index = 1
		self.headings = []

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


		# adding event bindings

		# a binding to close the sidePanel if it is shown, when the user clicks on any widget in the main panel
		self.bind("<Button-1>", self.focus_panel)
		self.buttons_container.bind("<Button-1>", self.focus_panel)
		self.column_container.bind("<Button-1>", self.focus_panel)

		self.place(relx = self.settings["main_panel_pos"][0], rely = self.settings["main_panel_pos"][1], relwidth = self.settings["main_panel_dimensions"][0], relheight = self.settings["main_panel_dimensions"][1])

	# adds a column to the GUI column container, returns a true if column was succesfully added
	# else false
	def add_column(self, name : str, data_type : str, lower : int, upper : int) -> bool:
		for heading in self.headings:
			if heading.get_name() == name: return False

		temp = ColumnHeading(self.column_container, self.settings, name, data_type, lower, upper, self.index, self)
		self.index += 1
		self.headings.append(temp)
		return True

	# deletes all the columns from the column container
	def reset_columns(self) -> None:
		self.headings = []
		for child in self.column_container.winfo_children():
			child.destroy()

	# deletes a specific column/columns from the column container
	def delete_column(self, index : int | List[int]) -> None:
		pass

	# hides the side panel
	def focus_panel(self, event):
		if self.master.side_panel.is_shown():
			self.master.side_panel.move()