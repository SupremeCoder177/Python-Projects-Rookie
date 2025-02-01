# File Extractor Version 2.0

# imports
import customtkinter as ctk
from darkdetect import isDark
from tkinter import messagebox, filedialog
from widgets import Label, Button, Entry, ListScrolledView, data, HoverFrame
from json import load
import logging
import os
import shutil
import threading


'''Main Class To Contain App Logic And UI'''
class App(ctk.CTk):

	def __init__(self, size : tuple) -> None:
		super().__init__()
		# setting theme to user pref
		ctk.set_appearance_mode('dark' if isDark() else 'light')

		# settings and logger for debugging
		self.logger = logging.getLogger(__name__)
		self.logger.setLevel("DEBUG")
		logging.basicConfig(filename="dummy.log",
			filemode = 'w',
			format = "%(message)s, at time %(asctime)s")
		self.logger.info("App is starting")

		# centering the app window
		x = (self.winfo_screenwidth() - size[0]) // 2
		y = (self.winfo_screenheight() - size[1]) // 2

		# settings window attributes
		self.title("File Extractor 2.0")
		self.geometry(f'{size[0]}x{size[1]}+{x}+{y}')
		self.resizable(False, False)

		# theme var
		self.is_dark = isDark()

		# setting stop event for algorithm
		self.stop_event = threading.Event()

		# pause vars for thread
		self.paused = False

		# thread for algorithm
		self.thread = None

		# making the UI
		self.add_widgets()

		# making sure the user can exit if the app freezed unexpectedly
		self.bind('<Escape>', lambda event: self.quit())
		self.logger.info("App is initialized")
		self.mainloop()

	'''Function to build the UI'''
	def add_widgets(self) -> None:
		# settings the app layout
		self.columnconfigure((0, 1), weight = 1, uniform = 'a')
		self.rowconfigure((0, 1), weight = 2, uniform = 'a')
		self.rowconfigure(2, weight = 3, uniform = 'a')

		# vars
		self.extract_from_path = ctk.StringVar(value = "Enter Path Here")
		self.extract_to_path = ctk.StringVar(value = "Enter Path Here")
		self.curr_extension = ctk.StringVar()
		self.extensions = []

		# frames
		extract_frame = HoverFrame(self)
		dst_frame = HoverFrame(self)
		get_extension_frame = HoverFrame(self)
		set_extension_frame = HoverFrame(self)
		run_frame = HoverFrame(self)
		info_frame = HoverFrame(self)

		self.logger.debug("All good while setting layout variables")
		self.logger.info("Adding widgets")

		# adding widgets to the frames
		Label(15, "Enter Path To\nExtract Files From", extract_frame).place(relx = 0.1, rely = 0.1, relwidth = 0.8)
		Label(15, "Enter Path\nTo Extract To", dst_frame).place(relx = 0.1, rely = 0.1, relwidth = 0.8)

		# entries for paths
		tmp = Entry(20, extract_frame, self.extract_from_path)
		tmp.bind('<Button-1>', lambda event: self.extract_from_path.set("" if not os.path.exists(self.extract_from_path.get()) else self.extract_from_path.get()))
		tmp.place(relx = 0.05, rely = 0.5, relwidth = 0.6)
		tmp = Entry(20, dst_frame, self.extract_to_path)
		tmp.bind('<Button-1>', lambda event: self.extract_to_path.set("" if not os.path.exists(self.extract_to_path.get()) else self.extract_to_path.get()))
		tmp.place(relx = 0.05, rely = 0.5, relwidth = 0.6)

		# buttons to browse paths for user convenience
		Button(12, "Browse", extract_frame, lambda: self.get_path(self.extract_from_path)).place(relx = 0.7, rely = 0.5, relwidth = 0.2)
		Button(12, "Browse", dst_frame, lambda: self.get_path(self.extract_to_path)).place(relx = 0.7, rely = 0.5, relwidth = 0.2)

		# extension input frame widgets
		Label(15, "Enter Extension Name Here", get_extension_frame).place(relx = 0.05, rely = 0.1, relwidth = 0.9)
		Entry(20, get_extension_frame, self.curr_extension).place(relx = 0.1, rely = 0.3, relwidth = 0.8)
		Button(15, "Add", get_extension_frame, self.add_ext).place(relx = 0.5, rely = 0.6, anchor = 'n')

		# all search extensions widgets frame 
		self.ext_view = ListScrolledView(set_extension_frame)
		self.ext_view.place(relx = 0.25, rely = 0.02, relwidth = 0.5, relheight = 0.8)
		Button(15, "Delete", set_extension_frame, self.rmv_ext).place(relx = 0.5, rely = 0.85, relwidth = 0.4, relheight = 0.15, anchor = 'n')

		# label to display warning when user enters incorrect data
		self.war_label = Label(12, "", get_extension_frame)
		self.war_label.configure(fg_color = "transparent")

		# run buttons
		self.start_btn = Button(20, "Start", run_frame, self.start)
		self.stop_btn = Button(20, "Stop", run_frame, self.stop)
		self.terminate_btn = Button(20, "Terminate", run_frame, self.refresh)
		self.stop_btn.configure(state = 'disabled')
		self.terminate_btn.configure(state = 'disabled')
		self.start_btn.place(relx = 0.5, rely = 0.1, anchor = 'n')
		self.stop_btn.place(relx = 0.5, rely = 0.3, anchor = 'n')
		self.terminate_btn.place(relx = 0.5, rely = 0.5, anchor = 'n')
		self.anim_label = Label(20, "", run_frame)

		# info labels
		self.found_files_label = Label(20, "No Of Files Found :", info_frame)
		self.err_files = Label(20, "Error Encountered :", info_frame)
		self.remain_files = Label(20, "Files Remaning :", info_frame)
		self.curr_file = Label(20, "Current File :", info_frame)
		self.found_files_label.place(relx = 0.0, rely = 0.1)
		self.err_files.place(relx = 0.0, rely = 0.25)
		self.curr_file.place(relx = 0.0, rely = 0.5)
		self.remain_files.place(relx = 0.0, rely = 0.65)

		# griding the frames
		extract_frame.grid(row = 0, column = 0, sticky = "NSEW", padx = data["frame_padding"], pady = data["frame_padding"])
		dst_frame.grid(row = 0, column = 1, sticky = "NSEW", padx = data["frame_padding"], pady = data["frame_padding"])
		get_extension_frame.grid(row = 1, column = 0, sticky = "NSEW", padx = data["frame_padding"], pady = data["frame_padding"])
		set_extension_frame.grid(row = 1, column = 1, sticky = "NSEW", padx = data["frame_padding"], pady = data["frame_padding"])
		run_frame.grid(row = 2, column = 0, sticky = "NSEW", padx = data["frame_padding"], pady = data["frame_padding"])
		info_frame.grid(row = 2, column = 1, sticky = "NSEW", padx = data["frame_padding"], pady = data["frame_padding"])

		# btn to toggle between dark mode and light mode 
		Button(5, "D/L", self, self.toggle_theme).place(relx = 1, rely = 1, anchor = 'se', relwidth = 0.04, relheight = 0.04)

		self.logger.info("UI is completed")

	# function to toggle themes
	def toggle_theme(self) -> None:
		if self.is_dark: 
			ctk.set_appearance_mode('light')
			self.is_dark = False
		else:
			ctk.set_appearance_mode('dark')
			self.is_dark = True

	# function to search all the files with gven extensions
	def search(self) -> None:
		# checking for invalid paths
		if self.extract_to_path.get() == self.extract_from_path.get():
			self.display_search_warning("Extract from, and\nextract to paths, cannot be same!", 2000)
			self.refresh()
			return
		if not (os.path.exists(self.extract_from_path.get()) and os.path.exists(self.extract_to_path.get())):
			self.display_search_warning("Invalid Path(s) !!", 2000)
			self.refresh()
			return
		if len(self.extensions) == 0:
			self.display_search_warning("No Extension Entered !", 2000)
			self.refresh()
			return

		# updating animated label
		self.anim_label.configure(text = "Searching")
		self.anim_label.place(relx = 0.5, rely = 0.7, anchor = 'n')
		paths = [self.extract_from_path.get()]
		files = []
		# performing a bfs search in the filesystem
		while paths:
			self.update_info_frame(str(len(files)), '0', "None", "Search", str(len(files)))
			temp = []
			for path in paths:
				try:
					for folder in os.listdir(path):
						if os.path.isdir(os.path.join(path, folder)): 
							temp.append(os.path.join(path, folder))
						else:
							if os.path.isfile(os.path.join(path, folder)):
								for ext in self.extensions:
									if folder.endswith(ext): files.append(os.path.join(path, folder))
				except Exception as e:
					self.logger.error(f"Found exception while trying to acces file/folder name {path}, exception name {e}")
			paths.clear()
			paths.extend(temp)
		self.logger.info(f"Found {len(files)}, preparing for extraction")
		self.extract(files)

	# function to copy files to specified path
	def extract(self, files : list) -> None:
		errs = 0
		count = len(files)
		for file in files:
			self.update_info_frame(str(len(files)), str(errs), file, "Extract", str(count))
			try:
				shutil.copy2(file, self.extract_to_path.get())
			except Exception as e: 
				self.logger.error(f"Found error with file {file}, error = {e}")
				errs += 1
			count -= 1
		self.logger.info(f"Completed extraction with {errs} erros during copying")
		messagebox.showinfo("Done !!", f"Files were extracted with {errs} errors\ncheck log file in folder for more info")
		self.refresh()

	# function to update the info labels and also animate the anim_label
	def update_info_frame(self, ffl : str, efl : str, cfl : str, al : str, rf : str) -> None:
		self.found_files_label.configure(text = f"No Of Files Found : {ffl}")
		self.err_files.configure(text = f"Error Encountered : {efl}")
		self.curr_file.configure(text = f"Current File : {cfl}")
		self.remain_files.configure(text = f"Files Remaning : {rf}")
		if al: self.anim(al)

	# function animate anim_label based on current thread execution
	def anim(self, task) -> None:
		if task == "Search":
			string = "Searching"
		else:
			string = "Extracting"
		count = self.anim_label.cget("text").count('.')
		count = 0 if count > 3 else count + 1
		for i in range(count): string += "."
		self.anim_label.configure(text = string)

	# function to initialize a new thread for execution
	def start(self) -> None:
		if not self.stop_event.is_set() and self.thread:
			self.paused = False
			return
		self.paused = False
		self.logger.info(f"Search begin for path {self.extract_from_path.get()} to {self.extract_to_path.get()}, for extensions {self.extensions}")
		self.stop_event.clear()
		self.thread = threading.Thread(target = self.search)
		self.thread.daemon = True
		self.thread.start()
		self.toggle_state([self.start_btn, self.stop_btn, self.terminate_btn])

	# halting the thread's execution until 
	def stop(self) -> None:
		self.logger.info("Search halted")
		self.toggle_state([self.start_btn, self.stop_btn, self.terminate_btn])
		self.paused = True
		while self.paused:
			self.stop_event.wait()

	# function for toggling button states
	def toggle_state(self, btns) -> None:
		for btn in btns:
			btn.configure(state = "disabled" if btn.cget("state") == 'normal' else "normal")

	def refresh(self):
		self.logger.info("Search terminated")
		self.stop_event.set()
		self.update_info_frame("", "", "None", "", "")
		self.thread = None
		self.anim_label.place_forget()

	# function to update textvariable with user chosen path
	def get_path(self, var) -> None:
		path = filedialog.askdirectory()
		if path:
			var.set(path)

	# function to delete extension from search list
	def rmv_ext(self) -> None:
		if self.ext_view.selected_label is None: return
		self.ext_view.delete_label(self.ext_view.selected_label.label.cget("text"))
		self.extensions.remove(self.ext_view.selected_label.label.cget("text"))
		self.ext_view.selected_label = None

	# function to display a warning label for given time when user enters invalid extension in entry
	def display_warning(self, text : str, time : int) -> None:
		self.war_label.configure(text = text)
		self.war_label.place(relx = 0.5, rely = 0.8, anchor = 'n')
		self.after(time, lambda: self.war_label.place_forget())

	# function to display a warning label when search is executed with wrong paths for given time
	def display_search_warning(self, text : str, time : int) -> None:
		self.anim_label.configure(text = text)
		self.anim_label.place(relx = 0.5, rely = 0.7, anchor = 'n')
		self.after(time, lambda: self.anim_label.place_forget())

	# function to add extensions for the algorithm to search for
	def add_ext(self):
		if len(self.curr_extension.get()) == 1 and self.curr_extension.get().startswith('.'):
			self.display_warning("Invalid Extension !!", 1500)
			return
		if not self.curr_extension.get():
			self.display_warning("No Extension Entered !!", 1500)
			return
		if not self.curr_extension.get().startswith('.'):
			self.display_warning("Invalid Extension Format !!", 1500)
			return
		if self.curr_extension.get() not in self.extensions: 
			self.extensions.append(self.curr_extension.get())
			self.ext_view.add_label(self.curr_extension.get(), 15)
		else: self.display_warning("Extension already in\nsearch list!", 1500)
			

# run
if __name__ == '__main__':
	# loading app settings from json file
	App((700, 600))
