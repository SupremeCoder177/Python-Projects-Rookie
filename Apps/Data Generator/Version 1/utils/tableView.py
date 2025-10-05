# this module handles the viewing of data

import customtkinter as ctk
from typing import List


class Table(ctk.CTkFrame):

	def __init__(self, master : ctk.CTkFrame, settings : dict):
		self.settings = settings
		super().__init__(master = master)

		# variables
		self.x = 0
		self.y = 0
		self.cell_width = 75
		self.max_cell_width = 200
		self.cell_height = 30
		self.scroll_speed = 10
		self.text_ids = list()

		# the canvas which will display the table
		self.canvas = ctk.CTkCanvas(self, scrollregion = (0, 0, self.winfo_width(), self.winfo_height()))
		self.canvas.pack(expand = True, fill = 'both', padx = 10, pady = 10)

		# event bindings
		self.canvas.bind_all("<MouseWheel>", self.move_y)
		self.canvas.bind_all("<Control-MouseWheel>", self.move_x)

		self.place(relx = self.settings["canvas_pos"][0], rely = self.settings["canvas_pos"][1], relwidth = self.settings["canvas_dimensions"][0], relheight = self.settings["canvas_dimensions"][1])

	# add a cell to the frame
	def add_cell(self, text : str) -> None:
		width = self.cell_width
		if len(text) > 15:
			width = self.max_cell_width

		self.canvas.create_rectangle((self.x, self.y, self.x + width, self.y + self.cell_height))
		_id = self.canvas.create_text(self.x + (width // 2), self.y + (self.cell_height // 2), anchor = "center", text = text, justify = "center", fill = "black")
		self.text_ids.append(_id)
		self.x += width

	# adds a row to the tableview
	def add_row(self, data : List[any]) -> None:
		for dat in data:
			self.add_cell(text = str(dat))

		# resetting the coordinate for the next row
		self.y += self.cell_height
		self.x = 0

	# deletes all the cells on the table
	def reset(self) -> None:
		for child in self.canvas.winfo_children():
			child.destroy()

	# moves all the cells vertically
	def move_y(self, event) -> None:
		if event.delta < 0:
			self.canvas.move("all", 0, -self.scroll_speed)
		else:
			self.canvas.move("all", 0, self.scroll_speed)

	# moves all the cells horizontally
	def move_x(self, event) -> None:
		if event.delta < 0:
			self.canvas.move("all", -self.scroll_speed, 0)
		else:
			self.canvas.move("all", self.scroll_speed, 0)


class TableView(ctk.CTkFrame):

	def __init__(self, master : ctk.CTk, settings : dict):
		super().__init__(master = master)

		# variables
		self.settings = settings
		self.max_rows = 200
		self.num_rows = 0

		# creating the labels
		ctk.CTkLabel(self,
			text = "Generated Table").place(relx = 0.1, rely = 0.02, relwidth = 0.8, relheight = 0.1)

		# creating the table
		self.table = Table(self, self.settings)

		self.place(relx = self.settings["table_view_pos"][0], rely = self.settings["table_view_pos"][1], relwidth = self.settings["table_view_dimensions"][0], relheight = self.settings["table_view_dimensions"][1])

	# clears the previous table
	def reset(self):
		self.table.reset()
		self.num_rows = 0

	# adds a row to the table, if the number of
	# rows in the table is less than max_rows
	# (too many entries causes the canvas to be laggy)
	def add_row(self, data : List[any]):
		if self.num_rows < self.max_rows:
			self.table.add_row(data)
			self.num_rows += 1
