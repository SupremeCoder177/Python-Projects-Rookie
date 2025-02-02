# Another anime app, because the one before sucks

import customtkinter as ctk
from darkdetect import isDark
from settings import *
from usables import *
import requests
from webbrowser import open_new_tab
from tkinter import messagebox


class App(ctk.CTk):

	def __init__(self, size : tuple):
		# initializations
		super().__init__()
		self.title("Anime 2.0")

		# centering the app
		x = (self.winfo_screenwidth() - size[0]) // 2
		y = (self.winfo_screenheight() - size[1]) // 2
		self.geometry(f'{size[0]}x{size[1]}+{x}+{y}')

		# variable to keep track of current theme
		self.is_dark = isDark()

		# adjusting theme to user prefrences
		if isDark(): 
			ctk.set_appearance_mode('dark') 
		else:
			ctk.set_appearance_mode('light')

		# all anime streaming websited dns
		self.sites = {"AnimeSuge" : "https://www.animesugetv.to", 
					  "HiAnime"   : "https://www.hianime.to", 
					  "AniWatch"  : "https://www.aniwatchtv.to"}

		# class instance to handle loading and uploading data
		self.data_manager = DataOrganizer(DATA_PATH["names"], DATA_PATH["desc"])

		# varaible holding current anime name
		self.selected_anime = ""

		# adding layout and widgets
		self.add_widgets()

		# making sure a sure fire way to exit the app if freezes
		self.bind("<Escape>", lambda event: self.quit())
		self.mainloop()

	# adding widgets to screen
	# this function calls some other function and only those widgets
	# which don't have a grid layout are placed using this method
	def add_widgets(self):
		# making an app font
		self.font = ctk.CTkFont(family = FONT_FAMILY, size = FONT_SIZE)

		# making a layout for all widgets
		self.rowconfigure(0, weight = 1, uniform = 'a')
		self.columnconfigure(0, weight = 3, uniform = 'a')
		self.columnconfigure(1, weight = 1, uniform = 'a')

		self.add_info_widgets()
		self.add_desc_widgets()

		''' This is an animated frame which if deafault off window
			on clicking a panel would appear with names of anime 
			streaming sited which user can click on to be directed to them
			to watch more anime, and keep expanding the list (hehe boi)
		'''
		# frame to hold all sites which user can use to watch anime
		self.anim_selection_frame = VerticalDropDown(self, 0, -0.36, 1 - (1 / 4), 1 / 4, 0.4)

		ctk.CTkLabel(self.anim_selection_frame, text = "Choose a site\nto watch more !!", font = self.font, fg_color = SITE_LABEL_BG, text_color = SITE_LABEL_TXT_CLR,
			corner_radius = 15).pack(expand = True)

		for site in self.sites:
			ctk.CTkButton(self.anim_selection_frame,
				text = site,
				font = self.font,
				fg_color = SITE_BTN_BG,
				hover_color = SITE_BTN_HVR_CLR,
				text_color = SITE_BTN_TXT_CLR,
				command = lambda site=site: self.open(self.sites[site])).pack(expand = True)

		self.anim_selection_frame.set_btn(DropDownButton(self.anim_selection_frame, "vertical", 0.3, 0))

		'''This panel is the one the user will use to add/delete a new anime to
		   their list
		'''

		self.anim_toggle_frame = HorizontalDropDown(parent = self, start_x = 0, end_x = -0.36, width = 0.4, height = 0.65, y = 0.2)
		tabs = ctk.CTkTabview(self.anim_toggle_frame, fg_color = 'transparent')
		tabs.add("Add")
		tabs.add("Delete")

		ctk.CTkLabel(tabs.tab("Delete"), text = "Anime Name", font = self.font,
			fg_color = ADD_LABEL_BG,
			text_color = ADD_LABEL_TXT_CLR,
			corner_radius = 20).pack(expand = True)

		self.del_anim_name = ctk.CTkEntry(tabs.tab("Delete"),
			fg_color = ADD_ENTRY_BG,
			text_color = ADD_ENTRY_TXT_CLR)
		self.del_anim_name.pack(expand = True, fill = 'x')

		ctk.CTkButton(tabs.tab("Delete"),
			text = "Delete",
			font = self.font,
			fg_color = ADD_BTN_BG,
			hover_color = ADD_BTN_HVR_CLR,
			text_color = ADD_BTN_TXT_CLR,
			command = self.delete_anime).pack(expand = True)

		self.warning_label = ctk.CTkLabel(tabs.tab("Delete"), text = "", font = self.font,
			fg_color = "transparent",
			text_color = ("#222", "#eee"),
			corner_radius = 20)
		self.warning_label.pack(expand = True)

		ctk.CTkLabel(tabs.tab("Add"), text = "Name of the Anime", font = self.font,
			fg_color = ADD_LABEL_BG,
			text_color = ADD_LABEL_TXT_CLR,
			corner_radius = 20).place(relx = 0.04, rely = 0.05, relwidth = 0.8, relheight = 0.07)

		self.new_anim_status = ctk.StringVar(value = "True")
		self.new_anim_type = ctk.StringVar(value = "Anime")

		self.new_anim_name = ctk.CTkEntry(tabs.tab("Add"),
			fg_color = ADD_ENTRY_BG,
			text_color = ADD_ENTRY_TXT_CLR)

		self.new_anim_name.place(relx = 0.04, rely = 0.13, relwidth = 0.8, relheight = 0.1)

		ctk.CTkLabel(tabs.tab("Add"), text = "Watch Status", font = self.font,
			fg_color = ADD_LABEL_BG,
			text_color = ADD_LABEL_TXT_CLR,
			corner_radius = 20).place(relx = 0.04, rely = 0.27, relwidth = 0.8, relheight = 0.07)

		ctk.CTkButton(tabs.tab("Add"),
			textvariable = self.new_anim_status,
			font = self.font,
			fg_color = ADD_BTN_BG,
			hover_color = ADD_BTN_HVR_CLR,
			text_color = ADD_BTN_TXT_CLR,
			command = lambda: self.new_anim_status.set("True" if self.new_anim_status.get() == "False" else "False")).place(relx = 0.04, rely = 0.37, relwidth = 0.8, relheight = 0.07)

		ctk.CTkLabel(tabs.tab("Add"), text = "Type", font = self.font,
			fg_color = ADD_LABEL_BG,
			text_color = ADD_LABEL_TXT_CLR,
			corner_radius = 20).place(relx = 0.04, rely = 0.5, relwidth = 0.8, relheight = 0.07)		

		ctk.CTkButton(tabs.tab("Add"),
			textvariable = self.new_anim_type,
			font = self.font,
			fg_color = ADD_BTN_BG,
			hover_color = ADD_BTN_HVR_CLR,
			text_color = ADD_BTN_TXT_CLR,
			command = lambda: self.new_anim_type.set("Movie" if self.new_anim_type.get() == "Anime" else "Anime")).place(relx = 0.04, rely = 0.59, relwidth = 0.8, relheight = 0.07)

		ctk.CTkButton(tabs.tab("Add"),
			text = "Add Anime",
			font = self.font,
			fg_color = ADD_BTN_BG,
			hover_color = ADD_BTN_HVR_CLR,
			text_color = ADD_BTN_TXT_CLR,
			command = self.add_anime).place(relx = 0.19, rely = 0.75, relwidth = 0.5, relheight = 0.07)

		tabs.pack(expand = True, fill = 'both')
		self.anim_toggle_frame.set_btn(DropDownButton(self.anim_toggle_frame, "horizontal", 0, -0.35))

		''' Nothing to document but just wanted to say, it took a lot of head-scratching figuring out a decent theme for light and dakr 
			I know I could have used ttkbootstrap but it is not nearly flexible enough for all the other
			custom widgets
		'''
		# button to toggle between light mode and dark mode
		ctk.CTkButton(self, text = "☢", 
			fg_color = THEME_BTN_CLR, 
			hover_color = THEME_BTN_HVR_CLR, 
			width = 25, 
			height = 25, 
			corner_radius = 10, 
			command = self.change_theme,
			text_color = THEME_BTN_TXT_CLR).place(relx = 0, rely = 1, anchor = "sw")

	def add_anime(self):
		if not self.new_anim_name.get(): return
		if self.new_anim_name.get() not in self.data_manager.format_dat.keys():
			self.data_manager.format_dat[self.new_anim_name.get()] = {"watched" : True if self.new_anim_status.get() == "True" else False,
																	  "type" : self.new_anim_type.get(),
																	  "desc" : "No Description Yet"}
			self.data_manager.update_anime_existence(self.new_anim_name.get())
			self.refresh_lists()

	def delete_anime(self):
		if not self.del_anim_name.get(): 
			self.warning_label.configure(text = "Enter a name !!")
			self.after(1500, lambda: self.warning_label.configure(text = ""))
			return
		if self.del_anim_name.get() not in self.data_manager.format_dat:
			self.warning_label.configure(text = "No Such Anime In List !!")
			self.after(1500, lambda: self.warning_label.configure(text = ""))
			return
		if not messagebox.askyesno("Warning !!", "Are you sure ?"): return
		self.data_manager.delete_anime(self.del_anim_name.get())
		self.refresh_lists()

	def open(self, url):
		try:
			request = requests.get(url, timeout = 5)
			if url.status_code == 200:
				print("run")
				open_new_tab(url)
			else:
				print("Errors")
				messagebox.showerror("Error", "The Site Couldn't Open")
		except Exception as e:
			if e == requests.ConnectionError:
				messagebox.showerror("Error", "Connect To Internet Bruh.")
				return

	def change_watch_status(self):
		if not self.selected_anime: return
		temp = self.data_manager.format_dat[self.selected_anime]["watched"]
		self.data_manager.format_dat[self.selected_anime]["watched"] = not temp
		self.load_anime_description(self.selected_anime)

	def add_desc_widgets(self):
		''' This frame represents the right side of the app
			user selected anime attributes will be loaded here 
			user can also alter the attributes
		'''

		# frame for loading selected anime attributes (description, type, and watch status)
		self.desc_frame = ctk.CTkFrame(self, fg_color = DESC_FRAME_BG)

		# info frame widgets

		# vars for holding selected anime info
		self.watch_status = ctk.StringVar(value = "Nothing")
		self.type = ctk.StringVar(value = "Nothing")
		self.curr_anime = ctk.StringVar(value = self.selected_anime)

		ctk.CTkLabel(self.desc_frame,
			text = "Selected Anime",
			font = self.font,
			fg_color = DESC_LABEL_BG,
			text_color = DESC_LABEL_TXT_CLR,
			corner_radius = 10,
			anchor = 'w').place(relx = 0.05, rely = 0.05, relwidth = 0.9, relheight = 0.05)

		BorderLabel(master = self.desc_frame, fg_color = DESC_LABEL_BG, text_color = DESC_LABEL_TXT_CLR, corner_radius = 0,
			font = self.font, textvariable = self.curr_anime,
			border_color = DESC_LABEL_BD_CLR,
			border_width = DESC_LABEL_BD_WIDTH,
			anchor = 'w').get_label().place(relx = 0.05, rely = 0.12, relwidth = 0.9, relheight = 0.05)


		ctk.CTkLabel(self.desc_frame, text = "Watched Status", font = self.font,
			fg_color = DESC_LABEL_BG,
			text_color = DESC_LABEL_TXT_CLR,
			corner_radius = 10,
			anchor = 'w').place(relx = 0.05, rely = 0.2, relwidth = 0.9, relheight = 0.05)

		''' BorderLabel is not a customtkinter class, it is a custom clas I made because the 
			customtkinter labels do not have a border option which I needed
			souce code in usables.py
		'''

		# frame to hold the actual label and button for toggling
		temp = ctk.CTkFrame(self.desc_frame, fg_color = "transparent")

		BorderLabel(master = temp, fg_color = DESC_LABEL_BG, text_color = DESC_LABEL_TXT_CLR, corner_radius = 0,
			font = self.font, textvariable = self.watch_status,
			border_color = DESC_LABEL_BD_CLR,
			border_width = DESC_LABEL_BD_WIDTH,
			anchor = 'center').get_label().pack(expand = True, fill = 'x', side = 'left', padx = WIDGET_PADDING['small'])

		ctk.CTkButton(temp, text = "T/F", fg_color = DESC_BTN_BG, font = self.font, hover_color = DESC_BTN_HVR_CLR, text_color = DESC_BTN_TXT_CLR,
			command = self.change_watch_status,
			width = 10, height = 10).pack(side = 'left')
		temp.place(relx = 0.05, rely = 0.27, relwidth = 0.9, relheight = 0.05)

		ctk.CTkLabel(self.desc_frame, text = "Type :", font = self.font,
			fg_color = DESC_LABEL_BG,
			text_color = DESC_LABEL_TXT_CLR,
			corner_radius = 10,
			anchor = 'w').place(relx = 0.05, rely = 0.35, relwidth = 0.9, relheight = 0.05)

		BorderLabel(master = self.desc_frame, fg_color = DESC_LABEL_BG, text_color = DESC_LABEL_TXT_CLR, corner_radius = 0,
			font = self.font, textvariable = self.type,
			border_color = DESC_LABEL_BD_CLR,
			border_width = DESC_LABEL_BD_WIDTH,
			anchor = 'center').get_label().place(relx = 0.05, rely = 0.42, relwidth = 0.9, relheight = 0.05)

		self.text = ctk.CTkTextbox(self.desc_frame, fg_color = DESC_TXT_BOX_BG, text_color = DESC_TXT_BOX_TXT_CLR)
		self.text.place(relx = 0.07, rely = 0.5, relwidth = 0.86, relheight = 0.4)

		ctk.CTkButton(self.desc_frame, text = "Save Changes", font = self.font,
			fg_color = DESC_BTN_BG,
			hover_color = DESC_BTN_HVR_CLR,
			text_color = DESC_BTN_TXT_CLR,
			command = self.save).place(relx = 0.1, rely = 0.92, relwidth = 0.8, relheight = 0.07)

		self.desc_frame.grid(row = 0, column = 1, sticky = "NSEW")

	def save(self):
		if not self.selected_anime: return
		desc = self.text.get("1.0", "end")
		self.data_manager.format_dat[self.selected_anime]["desc"] = desc
		self.data_manager.update_desc()
		self.data_manager.format_dat[self.selected_anime]["watched"] = True if self.watch_status.get() == "True" else False
		self.data_manager.update_names()
		self.refresh_lists()
		self.data_manager.upload()

	def refresh_lists(self):
		self.watched_list.clear()
		self.not_watched_list.clear()
		self.add_animes()

	def add_info_widgets(self):
		''' This frame represents the left side of the
			app and only holds a couple of widgets to load
			all the anime names whether watched or not
			user can click on any anime and its attributes will
			be loaded in the desc_frame (see below)
		'''

		# frame to hold all the anime lists
		self.anime_frame = ctk.CTkFrame(self, fg_color = FRAME_BG)

		# adding sub layout for better structure
		self.anime_frame.rowconfigure(0, weight = 1, uniform = 'b')
		self.anime_frame.rowconfigure(1, weight = 6, uniform = 'b')
		self.anime_frame.columnconfigure((0, 1), weight = 1, uniform = 'b')

		# adding the listing widgets

		ctk.CTkLabel(self.anime_frame, fg_color = LIST_LABEL_BG, text = "Watched Anime\n/Movies List", font = self.font, corner_radius = 10).grid(row = 0, column = 0, sticky =  'NSEW')
		# this is a custom widget too btw, source code in usables.py
		self.watched_list = ScrolledListView(parent = self.anime_frame, fg_color = 'transparent')
		self.watched_list.get_frame().grid(row = 1, column = 0, sticky = "NS")

		ctk.CTkLabel(self.anime_frame, fg_color = LIST_LABEL_BG, text = "Not Watched Anime\n/Movies List", font = self.font, corner_radius = 10).grid(row = 0, column = 1, sticky = "NSEW")
		self.not_watched_list = ScrolledListView(parent = self.anime_frame, fg_color = "transparent")
		self.not_watched_list.get_frame().grid(row = 1, column = 1, sticky = "NS")
		self.anime_frame.grid(row = 0, column = 0, sticky = "NSEW", padx = FRAME_PADDING)
		self.add_animes()

	def add_animes(self):
		# adding all watched status anime to the watched list
		self.add_anime_list(self.watched_list, True)

		# adding all the not-watched status anime to not_watched_list
		self.add_anime_list(self.not_watched_list, False)
		
	def add_anime_list(self, list_name, watch_status):
		for anime in self.data_manager.format_dat.keys():
			if self.data_manager.format_dat[anime]["watched"] == watch_status:
				list_name.add_label(text = anime,
					fg_color = LIST_LABEL_BG_ACTUAL,
					hover_color = LIST_LABEL_HVR_CLR_ACTUAL,
					text_color = DESC_LABEL_TXT_CLR,
					command = lambda event, anime=anime: self.load_anime_description(anime),
					font = self.font)

	def load_anime_description(self, name):
		self.selected_anime = name
		self.text.delete("1.0", "end")
		data = self.data_manager.format_dat[name]
		self.watch_status.set(str(data["watched"]).capitalize())
		self.type.set(data["type"])
		self.text.insert("1.0", data["desc"])
		self.curr_anime.set(self.selected_anime)
		if not self.data_manager.format_dat[name]["watched"]: self.text.configure(state = "disabled")
		else: self.text.configure(state = "normal")

	# function for toggling themes
	def change_theme(self):
		if self.is_dark:
			ctk.set_appearance_mode('light')
			self.is_dark = False
		else:
			ctk.set_appearance_mode("dark")
			self.is_dark = True


if __name__ == '__main__':
	App(APP_SIZE)