# this module defines the GUI for the control panel

import customtkinter as ctk


# a custom widget to change cell size
class CustomWidget(ctk.CTkFrame):

	def __init__(self, master, var, settings, command):
		super().__init__(master = master)	

		# label to tell the user what this widget is for
		ctk.CTkLabel(self,
			text = "Change Cell Size Here:",
			font = ctk.CTkFont(family = settings["font"], size = 30),
			fg_color = "transparent").pack(pady = 10)

		# entry for user to type in cell size (it will only work if they type in integers)
		ctk.CTkEntry(self,
			textvariable = var,
			font = ctk.CTkFont(family = settings["font"], size = 20),
			fg_color = "transparent").pack(fill = 'x', pady = 10)

		# button to apply changes to cell size
		ctk.CTkButton(self,
			text = "Change",
			font = ctk.CTkFont(family = settings["font"], size = 20),
			fg_color = settings["btn_color"],
			hover_color = settings["btn_hover_color"],
			text_color = settings["btn_txt_color"],
			command = command).pack()

		# a label to tell the user that cell size has been changed
		self.msg_label = ctk.CTkLabel(self,
			text = "",
			fg_color = "transparent",
			font = ctk.CTkFont(family = settings["font"], size = 25))
		self.msg_label.pack(pady = 20)

	# shows a msg on the msg label
	def show_msg(self, msg, time):
		self.msg_label.configure(text = msg)
		self.master.after(time, lambda: self.msg_label.configure(text = ""))


class ControlPanel(ctk.CTkFrame):

	def __init__(self, master):
		super().__init__(master = master)
		self.settings = master.settings
		self.shown = False

		# variables
		self.var = ctk.StringVar(value = self.settings["cell_size"])
		self.file_name = None

		# defining the GUI layout
		self.columnconfigure((0, 1), weight = 1, uniform = 'a')
		self.rowconfigure(0, weight = 2, uniform = 'a')
		self.rowconfigure(1, weight = 3, uniform = 'a')
		self.rowconfigure((2, 3, 4), weight = 1, uniform = 'a')

		# adding widgets

		# custom frame widget to alter cell size
		self.custom = CustomWidget(self, self.var, self.settings, master.change_cell_size)
		self.custom.grid(row = 0, column = 0, columnspan = 2, sticky = "NSEW")

		# console to show errors
		self.console = ctk.CTkTextbox(self,
			font = ctk.CTkFont(family = self.settings["font"], size = 22),
			state = "disabled")
		self.console.grid(row = 1, column = 0, columnspan = 2, sticky = "NSEW")

		# a button to save and build level dependencies 
		ctk.CTkButton(self,
			text = "Save",
			font = ctk.CTkFont(family = self.settings["font"], size = 20),
			text_color = self.settings["btn_txt_color"],
			fg_color = self.settings["btn_color"],
			hover_color = self.settings["btn_hover_color"],
			width = self.settings["btn_size"][0],
			height = self.settings["btn_size"][1],
			command = self.get_file_name).grid(row = 2, column = 0, sticky = "NW")

		# a button to load a pre-build level (work in progress)
		ctk.CTkButton(self,
			text = "Load",
			font = ctk.CTkFont(family = self.settings["font"], size = 20),
			text_color = self.settings["btn_txt_color"],
			fg_color = self.settings["btn_color"],
			hover_color = self.settings["btn_hover_color"],
			width = self.settings["btn_size"][0],
			height = self.settings["btn_size"][1]).grid(row = 2, column = 1, sticky = "NE")

		self.grid_pos = ctk.CTkLabel(self,
			font = ctk.CTkFont(self.settings["font"], size = 25),
			text_color = self.settings["label_txt_color"],
			fg_color = self.settings["label_color"],
			corner_radius = 10)
		self.grid_pos.grid(row = 3, column = 0, columnspan = 2, sticky = "NSEW")

		self.world_pos = ctk.CTkLabel(self,
			font = ctk.CTkFont(self.settings["font"], size = 25),
			text_color = self.settings["label_txt_color"],
			fg_color = self.settings["label_color"],
			corner_radius = 10)
		self.world_pos.grid(row = 4, column = 0, columnspan = 2, sticky = "NSEW")

		self.place(relx = self.settings["control_panel_pos"][0], rely = self.settings["control_panel_pos"][1], relwidth = self.settings["control_panel_size"][0], relheight = self.settings["control_panel_size"][1])

	def get_file_name(self):
		user_input = ctk.CTkInputDialog(text = "Enter Level Name", title = "Level Name")
		if user_input:
			self.file_name = user_input.get_input()
			self.master.builder.finalize()

	def update_mouse_info(self):
		w_pos = self.master.world.get_world_pos()
		g_pos = self.master.world.get_grid_pos()
		self.grid_pos.configure(text = f"Grid Pos : {g_pos[0]}, {g_pos[1]}")
		self.world_pos.configure(text = f"World Pos : {w_pos[0]}, {w_pos[1]}")

