import customtkinter as ctk
from settings import *
import os
import json

# drop down menus

# pre defined button for drop down frames
class DropDownButton(ctk.CTkButton):

	def __init__(self, drop_down, orient, start, end):
		super().__init__(master = drop_down, fg_color = ANIM_FRAME_BTN_BG, hover_color = ANIM_FRAME_BTN_HVR_CLR, font = ANIM_FRAME_BTN_FONT, command = drop_down.animate)
		if orient == 'vertical':
			self.back = "↑" if start > end else "↓"
			self.forward = "↑" if start < end else "↓"
		else:
			self.back = "<" if start > end else ">"
			self.forward = "<" if start < end else ">"
		self.put(orient, start, end)

	# one time call function for putting button according to parent orientation and movement direction for user ease of use
	def put(self, orient, start, end):
		if orient == 'vertical':
			if start < end:
				self.place(relx = 0, rely = 0, relwidth = 1, relheight = BTN_THICKNESS, anchor = 'nw')
			else:
				self.place(relx = 0, rely = 1 - 0.12, relwidth = 1, relheight = BTN_THICKNESS, anchor = 'nw')
		else:
			if start < end:
				self.place(relx = 0, rely = 0, relwidth = BTN_THICKNESS, relheight = 1, anchor = 'nw')
			else:
				self.place(relx = 1 - 0.12, rely = 0, relwidth = BTN_THICKNESS, relheight = 1, anchor = "nw")

	# changing text according to drop down parent position
	def change_text(self):
		curr_txt = self.cget("text")
		if curr_txt == self.back:
			self.configure(text = self.forward)
		else:
			self.configure(text = self.back)

# basic animated drop down class
class DropDown(ctk.CTkFrame):

	def __init__(self, parent, start, end, other_coor, width, height, orient, shown=False):
		super().__init__(master = parent, fg_color = ANIM_FRAME_BG, border_color = ANIM_FRAME_BD_CLR, border_width = ANIM_FRAME_BD_WIDTH)
		self.at_start = shown
		self.start = start
		self.end = end
		self.changing_coor = start if shown else end
		self.other_coor = other_coor
		self.orient = orient
		self.width = width
		self.height = height
		self.btn = None
		self.put()

	# giving a custom implementation of the default DropDownButton class to the menu
	def set_btn(self, btn):
		self.btn = btn
		if self.at_start: self.btn.configure(text = self.btn.back)
		else: self.btn.configure(text = self.btn.forward)

	# updaing position on screen after each frame
	def put(self):
		if self.orient == 'vertical':
			self.place(relx = self.other_coor, rely = self.changing_coor, relwidth = self.width, relheight = self.height)
		else:
			self.place(relx = self.changing_coor, rely = self.other_coor, relwidth = self.width, relheight = self.height)

	# animation logic for changing states
	def animate(self):
		if self.at_start:
			self.animate_back()
		else:
			self.animate_forward()

	# hiding the menu
	def animate_back(self):
		if self.changing_coor > self.end:
			self.changing_coor -= FRAME_DIFF
		if self.changing_coor < self.end:
			self.changing_coor += FRAME_DIFF
		self.put()
		if not self.end - TOLERANCE <= self.changing_coor <= self.end + TOLERANCE:
			self.after(ANIMATION_DELAY, self.animate_back)
		else:
			self.at_start = False
			# making sure the position isn't different because of floating point arithematic error
			self.changing_coor = self.end
			self.put()
			if self.btn: self.btn.change_text()

	# showing the menu
	def animate_forward(self):
		if self.changing_coor > self.start:
			self.changing_coor -= FRAME_DIFF
		if self.changing_coor < self.start:
			self.changing_coor += FRAME_DIFF
		self.put()
		if not self.start - TOLERANCE <= self.changing_coor <= self.start + TOLERANCE:
			self.after(ANIMATION_DELAY, self.animate_forward)
		else:
			self.at_start = True
			# making sure the position isn't different because of floating point arithematic error
			self.changing_coor = self.start
			self.put()
			if self.btn: self.btn.change_text()

# vertical implementation of drop down class
class VerticalDropDown(DropDown):
	def __init__(self, parent, start_y, end_y, x, width, height, shown=False):
		super().__init__(parent = parent, start = start_y, end = end_y, other_coor = x, width = width, height = height, shown = shown, orient = 'vertical')
	
# horizontal implementation of drop down class
class HorizontalDropDown(DropDown):
	def __init__(self, parent, start_x, end_x, y, width, height, shown=False):
		super().__init__(parent = parent, start = start_x, end = end_x, other_coor = y, width = width, height = height, shown = shown, orient = 'horizontal')

# organizing data of anime in usable format
class DataOrganizer:

	def __init__(self, names, desc):
		if not (os.path.exists(names) and os.path.exists(desc)):
			raise Exception("Bruh pls pass in valid data location")
		self.name_path = names
		self.desc_path = desc
		self.load_data()

	def load_data(self):
		try:
			with open(self.name_path, 'r') as f:
				self.names = json.load(f)
			with open(self.desc_path, 'r') as f:
				self.desc = json.load(f)
		except json.JSONDecodeError:
			raise Exception("Data not in proper format")
		self.format_data()

	def format_data(self):
		self.format_dat = dict()
		for name, list_ in self.names.items():
			watched = True if name not in  ("wanna_watch_list", "wanna_watch_list_movies") else False
			type_ = "Anime" if name not in ("watched_list_movies", "wanna_watch_list_movies") else "Movie"
			for anime in list_:
				self.format_dat[anime] = {"watched" : watched, "desc" : self.desc[anime], "type" : type_}

	def update_desc(self):
		for anime in self.format_dat:
			if self.format_dat[anime]["desc"] != self.desc[anime]:
				self.desc[anime] = self.format_dat[anime]["desc"]

	def search_anime_main_data_watch_status(self, anime):
		for list_ in self.names:
			for anime_ in self.names[list_]:
				if anime == anime_ and list_ in ("wanna_watch_list", "wanna_watch_list_movies"):
					return False
				if anime == anime_ and list_ in ("watched_list, watched_list_movies"):
					return True

	def update_anime_existence(self, anime):
		if anime not in self.desc.keys():
			self.desc[anime] = self.format_dat[anime]["desc"]
			if self.format_dat[anime]["type"] == "Anime" and self.format_dat[anime]["watched"]:
				self.names["watched_list"].append(anime)
			if self.format_dat[anime]["type"] == "Anime" and not self.format_dat[anime]["watched"]:
				self.names["wanna_watch_list"].append(anime)
			if self.format_dat[anime]["type"] == "Movie" and self.format_dat[anime]["watched"]:
				self.names["watched_list_movies"].append(anime)
			if self.format_dat[anime]["type"] == "Movie" and not self.format_dat[anime]["watched"]:
				self.names["wanna_watch_list_movies"].append(anime)
			self.upload()

	def delete_anime(self, anime):
		if anime not in self.format_dat: return
		del self.format_dat[anime]
		del self.desc[anime]
		for list_ in self.names.values():
			if anime in list_: list_.remove(anime)
		self.upload()

	def update_names(self):
		for anime in self.format_dat:
			if self.format_dat[anime]["watched"]:
				if not self.search_anime_main_data_watch_status(anime):
					if self.format_dat[anime]["type"] == "Anime":
						self.names["watched_list"].append(anime)
					else:
						self.names["watched_list_movies"].append(anime)
					if self.format_dat[anime]["type"] == "Anime":
						self.names["wanna_watch_list"].remove(anime)
					else:
						self.names["wanna_watch_list_movies"].remove(anime)
			else:
				if self.search_anime_main_data_watch_status(anime):
					if self.format_dat[anime]["type"] == "Anime":
						self.names["watched_list"].remove(anime)
					else:
						self.names["watched_list_movies"].remove(anime)
					if self.format_dat[anime]["type"] == "Anime":
						self.names["wanna_watch_list"].append(anime)
					else:
						self.names["wanna_watch_list_movies"].append(anime)

	def upload(self):
		try:
			with open(self.name_path, 'w') as f:
				json.dump(self.names, f, indent = 4, sort_keys = True)
			with open(self.desc_path, 'w') as f:
				json.dump(self.desc, f, indent = 4, sort_keys = True)
		except Exception as e:
			print(e)

# custom label with a border_color
class BorderLabel(ctk.CTkFrame):
	def __init__(self, master, textvariable, fg_color, text_color, font, border_color, corner_radius, border_width, anchor):
		super().__init__(master = master, fg_color = fg_color, border_color = border_color, border_width = border_width, corner_radius = corner_radius)
		ctk.CTkLabel(self, textvariable = textvariable, font = font, fg_color = 'transparent', anchor = anchor).pack(expand = True, fill = 'both')

	def get_label(self):
		return self


'''
This class is like a collection of buttons in a scrollable frame
but I like to labels more than button because they look cleaner
the labels looks and function exactly like buttons though
'''
# custom widget to represent a list as a scrollable frame labels with clickable event binding
class ScrolledListView(ctk.CTkScrollableFrame):

	def __init__(self, parent, fg_color):
		super().__init__(master = parent, fg_color = fg_color)

	def add_label(self, text, fg_color, hover_color, text_color, font, command):
		label = ctk.CTkLabel(self, text = text, fg_color = fg_color, font = font, text_color = text_color)
		label.configure(height = font.metrics("linespace") * 2)
		label.bind("<Enter>", lambda event: label.configure(fg_color = hover_color))
		label.bind("<Leave>", lambda event: label.configure(fg_color = fg_color))
		label.bind("<Button-1>", command)
		label.pack(fill = 'x')

	def get_frame(self):
		return self

	def clear(self):
		for child in self.winfo_children():
			child.destroy()


if __name__ == '__main__':
	dat = DataOrganizer('data/anim.json', 'data/desc.json')
