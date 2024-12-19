# Making a folder organizer in python

from settings import *


class App(ctk.CTk):

	def __init__(self):
		super().__init__(fg_color = APP_BG)
		self.title("File Organizer")
		self.iconbitmap('ICONS//icon.ico')
		self.resizable(False, False)

		# app positioning logic
		win_width = self.winfo_screenwidth()
		win_height = self.winfo_screenheight()

		x = (win_width - APP_SIZE[0]) // 2
		y = (win_height - APP_SIZE[1]) // 2

		self.geometry(f'{APP_SIZE[0]}x{APP_SIZE[1]}+{x}+{y}')

		self.add_widgets()


		self.bind('<Escape>', lambda event: self.quit())
		self.mainloop()

	def add_widgets(self):

		self.path_var = ctk.StringVar(value = 'Enter Path')
		self.rowconfigure(0, weight = 2, uniform = 'a')
		self.rowconfigure(1, weight = 1, uniform = 'a')
		self.columnconfigure(0, weight = 1, uniform = 'a')

		font = ctk.CTkFont(family = FONT, size = FONT_SIZE)

		frame = ctk.CTkFrame(self, fg_color = APP_BG)
		frame.columnconfigure(0, weight = 3, uniform = 'b')
		frame.columnconfigure(1, weight = 1, uniform = 'b')
		frame.rowconfigure(0, weight = 1, uniform = 'b')

		ctk.CTkEntry(frame,
			textvariable = self.path_var,
			font = font,
			fg_color = '#ccc',
			text_color = '#242424').grid(row = 0, column = 0, padx = PADDING, sticky = 'NSEW')

		ctk.CTkButton(frame,
			text = "Browse",
			font = font,
			fg_color = BTN_CLR,
			hover_color = BTN_HVR_CLR,
			command = self.get_path).grid(row = 0, column = 1)

		frame.grid(row = 0, column = 0, padx = PADDING)

		ctk.CTkButton(self,
			text = 'Organize',
			font = font,
			fg_color = BTN_CLR,
			hover_color = BTN_HVR_CLR,
			corner_radius = 10,
			command = self.organize).grid(row = 1, column = 0, padx = PADDING)

	def get_path(self):
		path = filedialog.askdirectory()
		if path:
			self.path_var.set(path)

	def organize(self):
		if not os.path.exists(self.path_var.get()): 
			self.path_var.set("No Such Directory")
			self.after(2000, lambda : self.path_var.set("Enter Path"))
			return

		files = os.listdir(self.path_var.get())
		files = [file for file in files if os.path.isfile(os.path.join(self.path_var.get(), file)) and file not in ['.gitignore']]

		unique_files = dict()

		for file in files:
			file_ext = os.path.splitext(file)[1]
			if file_ext in list(unique_files.keys()):
				temp = unique_files[file_ext]
				temp.append(os.path.join(self.path_var.get(), file))
				unique_files[file_ext] = temp
			else:
				unique_files[file_ext] = [os.path.join(self.path_var.get(), file)]

		for folder, files_ in unique_files.items():
			try:
				os.chdir(self.path_var.get())
				os.mkdir(folder[1:].capitalize() + " Files")
			except Exception as e:
				continue
			for file in files_:
				try:
					shutil.move(file, os.path.join(self.path_var.get(), folder[1:].capitalize() + " Files"))
				except Exception as e:
					continue


if __name__ == '__main__':
	App()