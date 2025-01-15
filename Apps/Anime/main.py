# Don't mind me just making another dumbshit program

import customtkinter as ctk
import requests
from tkinter import *
import json
from tkinter import ttk, messagebox
from webbrowser import open_new_tab


class App(ctk.CTk):

	def __init__(self, screen_size):
		super().__init__()

		x = (self.winfo_screenwidth() - screen_size[0]) // 2
		y = (self.winfo_screenheight() - screen_size[1]) // 2

		self.geometry(f'{screen_size[0]}x{screen_size[1]}+{x}+{y}')
		self.title("Anime Things")
		self.resizable(False, False)
		ctk.set_appearance_mode('dark')
		self.load_data()

		self.add_widgets()

		self.bind("<Escape>", lambda event: self.quit())
		self.attributes('-topmost', True)
		self.mainloop()

	def load_data(self):
		with open('data/desc.json', 'r') as f:
			self.desc = json.load(f)

		with open('data/anim.json', 'r') as f:
			temp = json.load(f)
		if not f.closed: f.close()

		self.ANIM_LISTS = {}
		count = 0
		for lis in temp.values():
			self.ANIM_LISTS[count] = lis
			count += 1

	def add_widgets(self):

		text_font = ctk.CTkFont(family = 'Cascadia Mono', size = 15)

		self.columnconfigure(0, weight = 2, uniform = 'c')
		self.columnconfigure(1, weight = 1, uniform = 'c')
		self.rowconfigure(0, weight = 1, uniform = 'c')

		input_frame = ctk.CTkFrame(self, fg_color = '#1d1b1f',
			 corner_radius = 20)

		desc_frame = ctk.CTkFrame(self, fg_color = 'transparent')

		input_frame.rowconfigure((0, 1, 2, 3), weight = 1, uniform = 'a')
		input_frame.columnconfigure((0, 1), weight = 1, uniform = 'a')

		btn_frame = ctk.CTkFrame(input_frame, fg_color = 'transparent')
		self.current_var = ''

		for index in self.ANIM_LISTS:	
			ctk.CTkComboBox(input_frame,
				values = sorted(self.ANIM_LISTS[index]),
				corner_radius = 10,
				fg_color = '#eee',
				text_color = '#111',
				dropdown_fg_color = '#232224',
				dropdown_hover_color = '#121112',
				dropdown_text_color = '#eee',
				command = lambda event: self.load_desc(event)).grid(row = index, column = 1, padx = 10, pady = 10, sticky = 'EW')

		ctk.CTkLabel(input_frame,
			text = "Watched List",
			font = text_font).grid(row = 1, column = 0)

		ctk.CTkLabel(input_frame,
			text = "Wanna Watch List",
			font = text_font).grid(row = 0, column = 0)

		ctk.CTkLabel(input_frame,
			text = "Watched List (Movies)",
			font = text_font).grid(row = 2, column = 0)

		ctk.CTkButton(btn_frame,
			text = "Watch",
			font = text_font,
			fg_color = '#1dcf8a',
			hover_color = '#16a66e',
			text_color = '#111',
			corner_radius = 10,
			command = self.watch).pack(expand = True)

		ctk.CTkLabel(desc_frame,
			text = "Description",
			font = text_font).pack(pady = 4)

		self.text = ctk.CTkTextbox(desc_frame,
			fg_color = '#eee',
			text_color = '#111',
			activate_scrollbars = False)

		self.text.pack(expand = True, fill = 'both', padx = 4, pady = 4)

		ctk.CTkButton(desc_frame,
			text = 'Save Changes',
			font = text_font,
			fg_color = '#1dcf8a',
			hover_color = '#16a66e',
			text_color = '#111',
			corner_radius = 5,
			command = self.save_changes).pack(expand = True)

		btn_frame.grid(row = 3, column = 0, columnspan = 2, sticky = 'NSEW')
		input_frame.grid(row = 0, column = 0, sticky = "NSEW", padx = 4)
		desc_frame.grid(row = 0, column = 1, sticky = 'NSEW', padx = 4)

	def load_desc(self, var):
		self.text.delete('1.0', 'end')
		self.current_var = var
		if var not in self.desc:
			self.text.insert('0.0', "Didn't Watch Yet so no description yet bruh.")
			return
		self.text.insert('0.0', self.desc[var])

	def save_changes(self):
		if self.current_var in self.desc:
			self.desc[self.current_var] = self.text.get('1.0', 'end')
		with open('data/desc.json', 'w') as file:
			json.dump(self.desc, file, indent = 4, sort_keys = True)
		with open('data/desc.json', 'r') as file:
			self.desc = json.load(file)
		if not file.closed: file.close()

	def watch(self):
		urls = ["https://animesugetv.to", "https://hianime.to", "https://aniwatchtv.to"]
		
		for url in urls:
			try:
				request = requests.get(url, timeout = 5)
				if request.status_code == 200:
					open_new_tab(url)
					return
				else: continue
			except Exception as e:
				if e == requests.ConnectionError:
					messagebox.showerror("Error", "No Internet Connection !!")
					return

		messagebox.showerror("Error", "No Working Site Found !!")


if __name__ == '__main__':
	App((700, 400))
