# Making a table viewing and editing app

import customtkinter as ctk
from widgets import FrameLabel
from animations import Move
import matplotlib as mat

'''
The reason this class takes in the whole data is because
there are so many customizations that it would not make any sense
to take each cuztomization as an argument
'''
class Viewer(ctk.CTkScrollableFrame):

	def __init__(self, master : ctk.CTk, fields : list[str], data : dict, axis : str, shown=False, pos_axis=True, time=300):
		super().__init__(master = master, fg_color = data["view_bg"], corner_radius = 20, border_color = data["view_bd_clr"], border_width = data["view_bd_width"])

		self.end = 1 if pos_axis else 0 - (data["view_width"] if axis == "horizontal" else data["view_height"])
		self.start = 0
		self.start_x = 0
		self.start_y = 0
		self.data = data
		self.time = time
		self.shown = shown
		self.fields = fields
		self.offset_x = self.offset_y = 0

		if self.shown:
			self.x = 0
			self.y = 0
		else:
			self.x = self.end if axis == "horizontal" else 0
			self.y = self.end if axis != "horizontal" else 0

		self.axis = axis
		self.anim_started = False
		self.add_widgets()

		self.place(relx = self.x, rely = self.y, relwidth = data["view_width"], relheight = data["view_height"])

	# triggers the widget animation
	def toggle_animation(self) -> None:
		if self.anim_started: return
		self.anim_started = True
		end = self.end if self.shown else self.start
		Move().move_widget(self.master, self, self.x, self.y, end, self.axis, self.data["view_width"], self.data["view_height"], self.time, self.anim_callback)

	# function to add the cells of the table and their data
	def add_widgets(self):
		for field in self.fields:
			label = ctk.CTkLabel(self,
				text = field,
				font = ctk.CTkFont(family = self.data["font"], size = self.data["view_font_size"]),
				fg_color = self.data["view_field_names_bg"],
				text_color = self.data["view_field_names_txt_clr"])
			self.add_cell(label)

	# adds all the UI interactions of the cells
	def add_interactions(self):
		pass

	# adds a cell a set size into the table
	# WARNING : only works with widgets whose master is self
	def add_cell(self, widget):
		# placing the widget in current next empty cell in row
		widget.place(relx = self.offset_x, rely = self.offset_y, relwidth = self.data["view_cell_width"], relheight = self.data["view_cell_height"])

		# increase the column index
		self.offset_x += self.data["view_cell_width"]
		# increase the row index if run out of columns and reset to 0 column
		if self.offset_x >= 1:
			self.offset_x = 0
			self.offset_y += self.data["view_cell_height"]

	def anim_callback(self):
		self.anim_started = False
		self.shown = not self.shown

		if self.shown:
			self.x = self.start_x
			self.y = self.start_y
		else:
			self.x = self.end if self.axis == "horizontal" else 0
			self.y = self.end if self.axis != "horizontal" else 0 


