# Making a file searcher app in python

from settings import *

class App(ctk.CTk):

	def __init__(self):
		super().__init__(fg_color = APP_BG)

		# app positioning logic
		win_width = self.winfo_screenwidth()
		win_height = self.winfo_screenheight()

		x = (win_width - APP_SIZE[0]) // 2
		y = (win_height - APP_SIZE[1]) // 2

		self.title("File Finder")
		self.iconbitmap('ICONS\\icon.ico')
		self.geometry(f'{APP_SIZE[0]}x{APP_SIZE[1]}+{x}+{y}')
		self.stop_thread = threading.Event()
		self.dot_count = 0

		self.add_widgets()

		self.bind('<Escape>', lambda event: self.quit())
		self.mainloop()

	def add_widgets(self):
		drives = self.get_drives()

		label_font = ctk.CTkFont(family = FONT, size = LABEL_FONT_SIZE)
		entry_font = ctk.CTkFont(family = FONT, size = ENTRY_FONT_SIZE)
		combobox_font = ctk.CTkFont(family = FONT, size = COMBO_FONT_SIZE)
		btn_font = ctk.CTkFont(family = FONT, size = BTN_FONT_SIZE)

		self.disk_var = ctk.StringVar(value = drives[0])
		self.file_var = ctk.StringVar(value = "Enter File Name")
		self.path_var = ctk.StringVar(value = '')
		self.input_frame = ctk.CTkFrame(self, fg_color = FRAME_BG)
		self.output_frame = ctk.CTkFrame(self, fg_color = FRAME_BG)

		ctk.CTkLabel(self.input_frame, 
			text = "Select Disk",
			fg_color = LABEL_COLOR,
			font = label_font,
			corner_radius = LABEL_CORNER_RADIUS).place(relx = 0.5, rely = 0.05, anchor = 'n', relwidth = 0.5, relheight = 0.2)

		ctk.CTkComboBox(self.input_frame,
			values = drives,
			variable = self.disk_var,
			font = combobox_font).place(relx = 0.5, rely = 0.25, anchor = 'n', relwidth = 0.3, relheight = 0.1)

		ctk.CTkEntry(self.input_frame,
			textvariable = self.file_var,
			font = entry_font).place(relx = 0.5, rely = 0.5, relwidth = 0.4, anchor = 'n', relheight = 0.2)

		self.search_btn = ctk.CTkButton(self.input_frame,
			text = "Search",
			font = btn_font,
			fg_color = BTN_COLOR,
			hover_color = BTN_HVR_CLR,
			command = self.change_btn_state)

		self.search_btn.place(relx = 0.2, rely = 0.7, anchor = 'nw', relwidth = 0.3)

		self.cancel_btn = ctk.CTkButton(self.input_frame,
			text = "Cancel",
			font = btn_font,
			fg_color = BTN_COLOR,
			hover_color = BTN_HVR_CLR,
			command = self.stop_thread.set,
			state = 'disabled')
		self.cancel_btn.place(relx = 0.5, rely = 0.7, anchor = 'nw', relwidth = 0.3)

		self.output_label = ctk.CTkLabel(self.output_frame,
			font = label_font,
			fg_color = FRAME_BG,
			corner_radius = LABEL_CORNER_RADIUS,
			textvariable = self.path_var)

		self.output_label.pack(expand = True, fill = 'both')

		self.input_frame.pack(padx = PADDING, pady = PADDING, expand = True, fill = 'both')
		self.output_frame.pack(expand = True, fill = 'both', padx = PADDING, pady = PADDING)

	def get_drives(self):
		return [f'{char}:\\' for char in string.ascii_uppercase if os.path.exists(f'{char}:\\')] if os.name == 'nt' else ['\\']

	def change_btn_state(self):
		self.after(0, lambda: self.cancel_btn.configure(state='disabled'))
		self.after(0, lambda: self.search_btn.configure(state='normal'))
		self.thread_search()

	def thread_search(self):
		self.thread = threading.Thread(target = self.search)
		animate_thread = threading.Thread(target = self.animate_search_label)
		animate_thread.daemon = True
		self.thread.daemon = True
		self.thread.start()
		animate_thread.start()

	def search(self):
		self.stop_thread.clear()
		file = self.file_var.get()
		disk = self.disk_var.get()
		paths = dict()
		paths.update({disk : "dir"})
		found = False
		output = None
		while paths:
			if self.stop_thread.is_set():
				self.cancel_btn['state'] = 'disabled'
				self.search_btn['state'] = 'normal'
				self.path_var.set('')
				break

			temp = dict()
			for path in paths.keys():
				try:
					folders = os.listdir(path)
				except Exception as e:
					continue
				for folder in folders:
					if os.path.isdir(os.path.join(path, folder)):
						temp[os.path.join(path, folder)] = 'dir'
					else:
						if folder == file:
							found = True
							output = os.path.join(path, folder)
				if found: break
			if found: break
			
			paths.clear()
			paths = temp.copy()

		if not output: 
			self.path_var.set("No Such File In Disk")
			self.after(1000, lambda: self.path_var.set(''))
		else:
			if os.name == 'nt':
				os.startfile(output)
			elif os.name == 'posix':
				subprocess.Popen(['xdg-open', path])
			self.after(1000, lambda: self.path_var.set(''))

	def animate_search_label(self):
		if not self.thread.is_alive(): return
		else: self.after(1000, self.animate_search_label)
		self.dot_count += 1
		if self.dot_count > 3: self.dot_count = 0
		dots = ''
		for i in range(self.dot_count):
			dots += '.'
		self.path_var.set("Searching" + dots)

		

if __name__ == '__main__':
	App()