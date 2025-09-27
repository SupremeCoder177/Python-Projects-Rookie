# this module handles the viewing of data

import customtkinter as ctk


class Table(ctk.CTkScrollableFrame):

	def __init__(self, master : ctk.CTkFrame, settings : dict):
		self.settings = settings
		super().__init__(master = master)

		# variables
		self.x = 0
		self.y = 0
		self.width = 0.2
		self.height = 0.1

		self.place(relx = self.settings["canvas_pos"][0], rely = self.settings["canvas_pos"][1], relwidth = self.settings["canvas_dimensions"][0], relheight = self.settings["canvas_dimensions"][1])

	# add a cell to the frame
	def add_cell(self, text : str) -> None:
		label = ctk.CTkLabel(self, text = text, fg_color = "#3F3244")
		label.place(relx = self.x, rely = self.y, relwidth = self.width, relheight = self.height)
		self.x += self.width

		# resetting the cell draw offset
		if self.x >= 1:
			self.y += self.height
			self.x = 0

	# deletes all the cells on the table
	def reset(self) -> None:
		for child in self.winfo_children():
			child.destroy()


class TableView(ctk.CTkFrame):

	def __init__(self, master : ctk.CTk, settings : dict):
		super().__init__(master = master)
		self.settings = settings

		# creating the labels
		ctk.CTkLabel(self,
			text = "Generated Table").place(relx = 0.1, rely = 0.02, relwidth = 0.8, relheight = 0.1)

		# creating the table
		self.table = Table(self, self.settings)

		self.place(relx = self.settings["table_view_pos"][0], rely = self.settings["table_view_pos"][1], relwidth = self.settings["table_view_dimensions"][0], relheight = self.settings["table_view_dimensions"][1])

