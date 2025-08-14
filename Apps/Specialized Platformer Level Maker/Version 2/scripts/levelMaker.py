# this module handles the loading of a pre-built level

from tkinter import filedialog, messagebox
import os
from json import load

class Maker:

	def __init__(self, app):
		self.app = app

	def load_level(self):
		path = filedialog.askdirectory()
		if path:
			jsons = list()

			# filtering all the items for only json files
			items = os.listdir(path)
			for item in items:
				if item.endswith(".json"):
					jsons.append(item)

			# trying to read each json file found for valid information
			temp = None
			for json in jsons:
				with open(os.path.join(path, json), "r") as f:
					temp = load(f)
					for item in temp.items():
						try:
							if len(item) != 3:
								break
							item["img_path"]
							item["img_size"]
							item["pos"]
						except Exception as e:
							temp = None
							break
			if not temp:
				# telling the user no valid jsons were
				self.app.show_err("No Valid Json files were found in the chosen folder.")
			else:
				self.app.show_err("Loading....")
				stack = messagebox.askyesno("Choose", "Do you want to stack this level or open fresh?")

				


		
