# this module handles the loading of a pre-built level

from tkinter import filedialog, messagebox
import os
from json import load

class Maker:

	def __init__(self, app):
		self.app = app

	def load_level(self):
		path = filedialog.askopenfilename()
		if path:	
			save_current = messagebox.askyesno("Choose", "Do you want to save the current file?")
			if save_current:
				while True:
					if self.app.control.get_file_name(): break
					if not messagebox.askretrycancel("File needs a name", "Please enter a name for the file to save it."): break

			data = None
			with open(path, "r") as f:
				data = load(f)
			self.app.show_err("Loading....")

			# loading the sprites
			if self.app.handler.get_images(data, os.path.split(path)[0]):
				self.app.side_panel.update(self.app.handler.sprites)
			else:
				self.app.show_err("Sprites could not be loaded !")

			# drawing the map on the world panel and updating info in the builder module
			self.app.world.draw_data(data)
			self.app.builder.add_data(data, path)
						

				


		
