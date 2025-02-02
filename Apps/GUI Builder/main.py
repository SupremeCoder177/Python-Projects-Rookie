# GUI Builder

import customtkinter as ctk
import os
import platform
import json
from tkinter import filedialog
from scripts.ctrl import Panel
from scripts.settings import *
from scripts.customizations import *

APP_SIZE = (1000, 800)


class App(ctk.CTk):

	def __init__(self, size):
		# init
		super().__init__()
		ctk.set_appearance_mode('dark')
		x = (self.winfo_screenwidth() - size[0]) // 2 if size[0] <= self.winfo_screenwidth() else 0
		y = (self.winfo_screenheight() - size[1]) // 2 if size[1] <= self.winfo_screenheight() else 0
		self.title("GUI Builder For Python")
		self.geometry(f'{size[0]}x{size[1]}+{x}+{y}')

		# vars
		self.size = size
		self.path = None
		self.attrs = {}
		
		# opening or creating a file
		self.ask_file()

		# run
		self.bind('<Escape>', lambda event: self.quit())
		self.mainloop()

	def ask_file(self):	
		[child.destroy() for child in self.winfo_children()]
		ctk.CTkButton(self,
			text = 'Open File',
			font = DEFAULT_FONT,
			fg_color = DEFAULT_BTN_CLR,
			hover_color = DEFAULT_BTN_HVR_CLR,
			command = lambda: self.open(filedialog.askdirectory()),
			corner_radius = 15).pack(side = 'left', expand = True)

		ctk.CTkButton(self,
			text = 'Create New',
			font = DEFAULT_FONT,
			fg_color = DEFAULT_BTN_CLR,
			hover_color = DEFAULT_BTN_HVR_CLR,
			command = lambda: self.make(filedialog.askdirectory()),
			corner_radius = 15).pack(side = 'left', expand = True)

	def open(self, path):
		if not path: return
		if not 'decompose.json' in os.listdir(path):
			temp = ctk.CTkLabel(self,
				text = 'No Decompose File Found In Folder !! Make Sure it is not in some other folder.',
				font = DEFAULT_FONT,
				fg_color = 'transparent')
			temp.place(relx = 0.5, rely = 0.8, anchor = 'center')
			self.after(2000, self.ask_file)
			return
		self.path = path
		with open(os.path.join(self.path, 'decompose.json'), 'r') as file:
			self.attrs = json.load(file)
		self.check_errs()
		self.emulate()

	def check_errs(self):
		if not self.attrs.get('import', None):
			self.attrs['import'] = ('Customtkinter')
		if not self.attrs.get('size', None):
			self.attrs['size'] = (self.size[0] * 0.8, self.size[1])

	def make(self, path):
		if not path: return
		self.path = path
		self.check_errs()
		self.emulate()

	def emulate(self):
		self.emulate_app_size_x = ctk.IntVar(value = self.attrs['size'][0])
		self.emulate_app_size_y = ctk.IntVar(value = self.attrs['size'][1])
		self.widget_size_x = ctk.IntVar(value = 20)
		self.widget_size_y = ctk.IntVar(value = 20)
		self.curr_color = 'red'
		self.curr_import = 'customtkinter'
		self.curr_widget = ctk.StringVar(value = 'BUTTON')

		[child.destroy() for child in self.winfo_children()]
		self.panel = Panel(self)
		self.app_space = ctk.CTkFrame(self, fg_color = '#222')
		self.app_space.grid(row = 0, column = 0, sticky = 'NSEW')
		self.customs = CustomizationsPanels(self)

	def save(self):
		try:
			with open(os.path.join(self.path, 'decompose.json'), 'w') as file:
				json.dump(self.attrs, file, indent = 4)
		except Exception as e:
			temp = ctk.CTkLabel(self,
				text = 'Internal System Error has Occurred !!',
				font = DEFAULT_FONT,
				fg_color = 'transparent')
			temp.place(relx = 0.5, rely = 0.8, anchor = 'center')
			self.after(2000, self.ask_file)


if __name__ == '__main__':
	App(APP_SIZE)
