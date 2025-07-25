# Making a GUI version of password generator

import customtkinter as ctk
from settings import *
from random import choice

class App(ctk.CTk):

	def __init__(self):
		super().__init__(fg_color = APP_BG)
		self.title("Password Generator")

		x = (self.winfo_screenwidth() - APP_SIZE[0]) // 2
		y = (self.winfo_screenheight() - APP_SIZE[1]) // 2

		self.geometry(f'{APP_SIZE[0]}x{APP_SIZE[1]}+{x}+{y}')
		self.resizable(False, False)

		self.add_widgets()

		self.bind('<Escape>', lambda event: self.quit())
		self.mainloop()

	def add_widgets(self):
		font = ctk.CTkFont(family = FONT, size = FONT_SIZE)
		in_fnt = ctk.CTkFont(family = FONT, size = INPUT_FONT_SIZE)

		self.length = ctk.StringVar(value = 10)
		self.output = ctk.StringVar(value = '')

		ctk.CTkLabel(self,
			text = "Enter Password Length",
			font = font,
			fg_color = APP_BG,
			text_color = TEXT_CLR).pack(padx = PADDING, pady = PADDING, expand = True)

		ctk.CTkEntry(self,
			textvariable = self.length,
			font = in_fnt,
			text_color = INPUT_TXT_CLR,
			fg_color = '#eee').pack(padx = PADDING, expand = True)

		ctk.CTkButton(self,
			text = "Generate",
			command = self.gen,
			font = in_fnt,
			text_color = INPUT_TXT_CLR,
			fg_color = BTN_CLR,
			hover_color = BTN_HVR_CLR).pack(expand = True, pady = PADDING)

		ctk.CTkLabel(self,
			textvariable = self.output,
			font = font,
			fg_color = APP_BG,
			text_color = TEXT_CLR).pack(padx = PADDING, expand = True)

	def gen(self):
		length = self.length.get()
		try:
			length = int(length)
		except Exception as e:
			self.output.set("Invalid Input !!")
			self.after(1500, lambda: self.output.set(''))

		if length < 8:
			self.output.set("Password length cannot be less than 10 !!")
			self.after(1500, lambda: self.output.set(''))
			return

		chars = [ch for ch in 'abcdefghijklmnopqrstuvwxyz1234567890-=+_~!@#$%^&*()']
		output = ''
		for i in range(length):
			output += choice(chars)
		self.output.set(output)


if __name__ == '__main__':
	App()