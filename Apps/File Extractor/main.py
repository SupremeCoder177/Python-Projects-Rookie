# File Extractor

import customtkinter as ctk
from tkinter import filedialog
from tkinter import messagebox
import shutil
import os
import threading

# App Settings
APP_SIZE = (400, 450)
BTN_BG = ("#baa90b", "#099414")
BTN_HVR_CLR = ("#857805", "#0cc41a")
BTN_TXT_CLR = ("#222", "#eee")
LABEL_BG = ("#099c99" ,"#150963")
LABEL_TXT_CLR = ("#222", "#eee")
FONT_FAMILY = "Helvetica"
FONT_SIZE = 15
ENTRY_BG = ("#222", "#eee")
ENTRY_TXT_CLR = ("#eee", "#222")



'''App class to contain all the logic and
   UI components
'''
class App(ctk.CTk):

	'''Simplpe Initialization of the UI'''
	def __init__(self, size : tuple) -> None:
		super().__init__()
		ctk.set_appearance_mode('dark')

		# centering the app window
		x = (self.winfo_screenwidth() - size[0]) // 2
		y = (self.winfo_screenheight() - size[1]) // 2

		self.title("Files Extractor")
		self.geometry(f"{size[0]}x{size[1]}+{x}+{y}")
		self.resizable(False, False)

		# extracting thread stop event
		self.stop_event = threading.Event()

		# adding the actual UI
		self.add_widgets()

		# making sure user can exit if app freezes unexpectedly
		self.bind("<Escape>", lambda event: self.quit())
		self.mainloop()

	def set_path(self, var):
		path = filedialog.askdirectory()
		if path:
			var.set(path)

	def label(self, text, x, y, width, height, master):
		ctk.CTkLabel(master = master,
			text = text,
			font = self.font,
			text_color = LABEL_TXT_CLR,
			fg_color = LABEL_BG,
			corner_radius = 10).place(relx = x, rely = y, relwidth = width, relheight = height)

	def entry(self, master, textvariable, width, check_txt):
		ent = ctk.CTkEntry(master = master,
			textvariable = textvariable,
			font = self.font,
			fg_color = ENTRY_BG,
			text_color = ENTRY_TXT_CLR,
			width = width)
		ent.pack(side = 'left', expand = True, padx = 2)
		ent.bind("<Button-1>", lambda event: textvariable.set("" if textvariable.get() == check_txt else textvariable.get()))

	def add_widgets(self):
		# font
		self.font = ctk.CTkFont(family = FONT_FAMILY, size = FONT_SIZE)

		# vars
		self.extract_path = ctk.StringVar(value = "Enter Path Here")
		self.extract_to_path = ctk.StringVar(value = "Enter Path Here")
		self.extension = ctk.StringVar()
		self.error = ctk.StringVar()
		extract_frame = ctk.CTkFrame(self, fg_color = 'transparent')
		extract_to_frame = ctk.CTkFrame(self, fg_color = 'transparent')

		# UI
		self.label("Choose Path To Extract From", 0.2, 0.1, 0.6, 0.07, self)

		self.entry(extract_frame, self.extract_path, 280, self.extract_path.get())
		ctk.CTkButton(master = extract_frame,
			text = "Browse",
			font = self.font,
			fg_color = BTN_BG,
			hover_color = BTN_HVR_CLR,
			text_color = BTN_TXT_CLR,
			corner_radius = 10,
			width = 20,
			command = lambda: self.set_path(self.extract_path)).pack(side = 'left')

		self.entry(extract_to_frame, self.extract_to_path, 280, self.extract_to_path.get())
		ctk.CTkButton(master = extract_to_frame,
			text = "Browse",
			font = self.font,
			fg_color = BTN_BG,
			hover_color = BTN_HVR_CLR,
			text_color = BTN_TXT_CLR,
			corner_radius = 10,
			width = 20,
			command = lambda: self.set_path(self.extract_to_path)).pack(side = 'left')
		
		extract_frame.place(relx = 0.05, rely = 0.2, relwidth = 0.9)
		self.label("Enter Path To Extract To", 0.2, 0.3, 0.6, 0.07, self)
		extract_to_frame.place(relx = 0.05, rely = 0.4, relwidth = 0.9)

		self.label("Enter Extension Here", 0.2, 0.5, 0.6, 0.07, self)
		ctk.CTkEntry(master = self,
			textvariable = self.extension,
			font = self.font,
			text_color = ENTRY_TXT_CLR,
			fg_color = ENTRY_BG).place(relx = 0.05, rely = 0.6, relwidth = 0.9)

		self.start_btn = ctk.CTkButton(master = self,
			text = "Extract",
			font = self.font,
			fg_color = BTN_BG,
			hover_color = BTN_HVR_CLR,
			text_color = BTN_TXT_CLR,
			corner_radius = 10,
			command = self.start)
		self.start_btn.place(relx = 0.5, rely = 0.7, anchor = 'n')

		self.err_label = ctk.CTkLabel(self,
			textvariable = self.error,
			fg_color = 'transparent',
			font = self.font).place(relx = 0.5, rely = 0.9, anchor = 'n')

		self.stop_btn = ctk.CTkButton(self,
			text = "Cancel",
			font = self.font,
			fg_color = BTN_BG,
			hover_color = BTN_HVR_CLR,
			text_color = BTN_TXT_CLR,
			command = lambda: self.stop_event.set())

	def start(self):
		self.start_btn.configure(state = 'disabled')
		self.stop_event.clear()
		self.thread = threading.Thread(target = self.extract)
		self.thread.daemon = True
		self.stop_btn.place(relx = 0.5, rely = 0.8, anchor = 'n')
		self.thread.start()

	def extract(self):
		if not self.extension.get().startswith('.'):
			self.error.set("Invalid Extension !")
			self.after(1500, lambda: self.error.set(""))
			self.stop_event.set()
			self.reset()
			return
		if self.extract_path.get() == self.extract_to_path.get():
			self.error.set("Cannot Extract From Same Location !")
			self.after(1500, lambda: self.error.set(""))
			self.stop_event.set()
			self.reset()
			return
		if not (os.path.exists(self.extract_path.get() and os.path.exists(self.extract_to_path.get()))):
			self.error.set("File Location Does Not Exist !")
			self.after(1500, lambda: self.error.set(""))
			self.stop_event.set()
			self.reset()
			return


		paths = [self.extract_path.get()]
		files = []
		self.after(0, lambda: self.error.set("Extracting..."))
		while paths:
			self.anim_search()
			if self.stop_event.is_set():
				self.stop_btn.place_forget()
				self.start_btn.configure(state = 'normal')
				return
			temp = []
			for path in paths:
				try:
					for folder in os.listdir(path):
						if os.path.isdir(os.path.join(path, folder)):
							temp.append(os.path.join(path, folder))
						else:
							if os.path.isfile(os.path.join(path, folder)):
								if folder.endswith(self.extension.get()):
									files.append(os.path.join(path, folder))
				except Exception as e: continue
			paths.clear()
			paths.extend(temp)
		self.copy_files(files, self.extract_to_path.get())
		self.after(0, lambda: self.error.set(""))
		self.reset()

	def reset(self):
		self.stop_btn.place_forget()
		self.start_btn.configure(state = 'normal')

	def copy_files(self, files, dst):
		for file in files:
			try:
				shutil.copy2(file, dst)
			except Exception as e:
				messagebox.showerror(f"Error Had Occured for file {file}", e)
				if not messagebox.askyeno("Do you want to continue ?"): break

	def anim_search(self):
		temp = self.error.get().count('.')
		if temp < 4: temp += 1
		else: temp = 0
		string = "Extracting"
		for i in range(temp): string += '.'
		self.error.set(string)


if __name__ == '__main__':
	App(APP_SIZE)