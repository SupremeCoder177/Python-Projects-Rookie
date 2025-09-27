# this module handles the viewing of data

import customtkinter as ctk


class TableView(ctk.CTkFrame):

	def __init__(self, master : ctk.CTk, settings : dict):
		super().__init__(master = master)
		self.settings = settings
