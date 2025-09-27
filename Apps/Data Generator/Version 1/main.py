# main file to handle all the API of this app

import customtkinter as ctk
from json import load
from darkdetect import isDark
from console import Console


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

		# settings the theme, if the them file is not present, then using default customtkiner themes
		try:
			ctk.set_default_color_theme("theme.json")
			print("sucessfully set custom theme")
		except FileNotFoundError as e:
			# setting the appropriate theme
			print("Couldn't load theme settings")
			ctk.set_appearance_mode("dark" if isDark() else "light")

		# setting window dimensions and position
		x = (self.winfo_screenwidth() - self.settings["app_size"][0]) // 2
		y = (self.winfo_screenheight() - self.settings["app_size"][1]) // 2
		self.geometry(f"{self.settings["app_size"][0]}x{self.settings["app_size"][1]}+{x}+{y}")

		# adding widgets

		# adding the console
		self.console = Console(self, self.settings)

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



if __name__ == "__main__":
	App()