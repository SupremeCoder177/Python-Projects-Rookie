# Making a specialized Editor for 2D games, it works with png images and divides
# the image in cells, each cell is a sprite which can be placed on the map
# multiple images can be loaded at once and unloaded as well.
# 
# The level information is saved in a json file, where each grid coordinate
# is linked with a file path to the png image where to find its sprite, and also
# the exact grid position of that sprite inside the png image.

# NOTE: If image paths are changed or deleted, the level file will not work with 
#       the upcoming app which will implement those level files in platformer levels.

# P.S. Yes this will also have a light mode version but I don't think I will ever use it

# this is the main app file

import customtkinter as ctk
from json import load
from darkdetect import isDark
from scripts.sidePanel import SidePanel

class App(ctk.CTk):

	def __init__(self):
		super().__init__()
		self.load_data()
		self.title("Specialized Platformer Level Maker")

		# changing theme according to current OS
		self.theme = "dark" if isDark() else "light"
		ctk.set_appearance_mode(self.theme)

		# settings the window size and position on screen
		size = self.settings["app_size"]
		x = (self.winfo_screenwidth() - size[0]) // 2 if size[0] < self.winfo_screenwidth() else 0
		y = (self.winfo_screenheight() - size[1]) // 2 if size[1] < self.winfo_screenheight() else 0
		self.geometry(f'{size[0]}x{size[1]}+{x}+{y}')

		# designing the layout of the app

		# side panel 
		# This will contain the loaded sprites and adding and deleting options
		# opening the control panel and changing theme modes
		self.side_panel = ctk.CTkFrame(self)

		# level simulator panel
		# This will be the level itself being shown in ctk.CTkCanvas mode (of course the actual level will be run in pygame)
		self.level_panel = ctk.CTkFrame(self,
			border_width = self.settings["level_panel_border_width"])

		# control panel
		# This panel will hold all the app settings, saving, opening a pre-built level
		# and also a console for displaying errors and current app info
		# it will be hidden at the start and will slide into view when pressed a button on the level_panel
		self.control_panel = ctk.CTkFrame(self)

		# applying default color themes to all panels
		self.set_panel_themes()

		# placing the panels on the app
		self.side_panel.place(relx = 0, rely = 0, relwidth = self.settings["side_panel_width"], relheight = self.settings["side_panel_height"])
		self.level_panel.place(relx = self.settings["level_panel_x"], rely = self.settings["level_panel_y"], relwidth = self.settings["level_panel_width"], relheight = self.settings["level_panel_height"])
		self.control_panel.place(relx = self.settings["control_panel_x"], rely = self.settings["control_panel_y"], relwidth = self.settings["control_panel_width"], relheight = self.settings["control_panel_height"])

		# sprite variables
		self.sprites = {}
		self.num_sprites = 0
		self.curr_sprite = None

		# adding GUI
		self.side = SidePanel(self.side_panel, self.settings)

		# only for debugging 
		self.bind('<Escape>', lambda event: self.quit())

	def load_data(self):
		with open("settings.json", "r") as f:
			self.settings = load(f)

	# sets all panels to initial theme
	def set_panel_themes(self):
		self.side_panel.configure(fg_color = self.settings["side_panel_color"])
		self.level_panel.configure(fg_color = self.settings["level_panel_color"],
			border_color = self.settings["level_panel_border_color"])
		self.control_panel.configure(fg_color = self.settings["control_panel_color"])	

	def change_theme(self):
		if self.theme == "light":
			ctk.set_appearance_mode("dark")
			self.theme = "dark"
		else:
			ctk.set_appearance_mode("light")
			self.theme = "light"

	def run(self):
		self.mainloop()

	def set_sprite(self, ind):
		self.curr_sprite = ind

	def del_sprite(self):
		if not self.curr_sprite: return
		if not self.curr_sprite in self.sprites: return
		del self.sprites[self.curr_sprite]
		self.num_sprites -= 1
		self.side.re_render_sprites()

	def del_sprites(self):
		self.num_sprites = 0
		self.sprites = {}
		self.side.re_render_sprites()

if __name__ == '__main__':
	a = App()
	a.run()