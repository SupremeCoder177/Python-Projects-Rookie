# main file to handle all the API of this app

import customtkinter as ctk
from json import load
from darkdetect import isDark
from console import Console
from tableView import TableView


# main app class
class App(ctk.CTk):

	# initializing the window and its components
	def __init__(self):

		if self.load_data():
			print("Settings loaded sucessfully, loading components...")
		else:
			print("Couldn't load settings, exiting...")

		# initializing tkinter and settings title
		super().__init__()
		self.title("CSV Data Generator")

		# variables
		self.theme = "light"

		ctk.set_appearance_mode(self.theme)

		# settings the theme, if the them file is not present, then using default customtkiner themes
		try:
			ctk.set_default_color_theme("theme.json")
			print("sucessfully set custom theme")
		except FileNotFoundError as e:
			print("Couldn't load theme settings")

		# setting window dimensions and position
		x = (self.winfo_screenwidth() - self.settings["app_size"][0]) // 2
		y = (self.winfo_screenheight() - self.settings["app_size"][1]) // 2
		self.geometry(f"{self.settings["app_size"][0]}x{self.settings["app_size"][1]}+{x}+{y}")

		# adding widgets

		# a button to toggle theme
		ctk.CTkButton(self,
			text = "T",
			command = self.theme_toggle).place(relx = 0, rely = 0.95, relwidth = 0.05, relheight = 0.05)

		# adding the console
		self.console = Console(self, self.settings)

		# adding the table view
		self.view = TableView(self, self.settings)

		self.bind("<Escape>", lambda event: self.quit())
		self.mainloop()

	# loads the json file which contains the app settings
	# the app will not start if the json file is missing
	# or the file doesn't have the necessary settings for the
	# app to function
	def load_data(self) -> bool:
		try:
			with open("settings.json", "r") as f:
				self.settings = load(f)
			return True
		except FileNotFoundError as e:
			return False

	# function to change the theme of the app from light to dark mode, or vice-versa
	def theme_toggle(self):
		self.theme = "dark" if self.theme == "light" else "light"
		ctk.set_appearance_mode(self.theme)


if __name__ == "__main__":
	App()