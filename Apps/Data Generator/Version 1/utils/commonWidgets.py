# This module defines the common widgets shared in the side-panel and main-panel

import customtkinter as ctk
from typing import List


# this class defines a label and an entry
class LabelEntry(ctk.CTkFrame):

	def __init__(self, master : ctk.CTkFrame, textvar : ctk.StringVar, text : str):
		super().__init__(master = master, fg_color = "transparent", border_width = 0)

		# the label
		ctk.CTkLabel(self,
			text = text).pack(fill = 'x', padx = 5, pady = 10)

		# the entry
		self.entry = ctk.CTkEntry(self,
			textvariable = textvar)
		self.entry.pack(fill = 'x', padx = 5)


# this class defines a label and an option menu
class LabelOptions(ctk.CTkFrame):

	def __init__(self, master : ctk.CTkFrame, options : List[any], textvar : ctk.StringVar, text : str):
		super().__init__(master = master, fg_color = "transparent", border_width = 0)

		# the label
		ctk.CTkLabel(self,
			text = text).pack(fill = 'x', padx = 5, pady = 10)

		# the option menu
		self.menu = ctk.CTkOptionMenu(self,
			values = options,
			variable = textvar,
			dynamic_resizing = True)
		self.menu.pack(fill = 'x', padx = 5)


