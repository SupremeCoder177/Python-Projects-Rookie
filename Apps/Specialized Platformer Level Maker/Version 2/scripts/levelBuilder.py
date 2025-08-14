# this module handles building the level file and its dependencies (aka sprites)

import json as j
import os
from tkinter import filedialog
from PIL import Image

class Builder:

	def __init__(self, app):
		self.app = app
		self.occupied = dict()
		self.stacked = list()
		self.nothing_changed = False

	# adds a cell to occupied
	def add_cell(self, pos):
		if pos not in self.occupied:
			self.nothing_changed = False
			img = self.app.handler.sprites[self.app.handler.curr_sprite]["sprite"]
			size = self.app.handler.sprites[self.app.handler.curr_sprite]["sprite_size"]
			self.occupied[pos] = {
				"sprite" : img,
				"size"  : size,
				"tag" : self.app.handler.curr_sprite
			}

	# deletes a cell from occupied 
	def delete_cell(self, pos):
		if pos in self.occupied:
			self.nothing_changed = False
			del self.occupied[pos]

	# builds level in json form and stores all images required
	def finalize(self):
		if self.nothing_changed: return
		path = filedialog.askdirectory()
		if path:
			name = self.app.control.file_name
			if not name:
				self.app.show_err("Enter the name of the level to save file !")
				return
			try:
				# making a directory to save the user images
				os.chdir(path)
				if f"{name} sprites" not in os.listdir():
					os.mkdir(f"{name} sprites")
				os.chdir(f"{name} sprites")
				invalids = ["/", ":", " ", "."]
				names = []
				# saving the images inside the directory
				for value in self.occupied.values():
					sprite_name = list()
					for ch in value["tag"]:
						if ch in invalids: continue
						else: sprite_name.append(ch)

					value["sprite"].save(f"{''.join(sprite_name)}.png")
					names.append(''.join(sprite_name))

				# getting back to path
				os.chdir(path)

				# dumping the occupied cell info into a json file
				temp = dict()
				count = 0
				for key, value in self.occupied.items():
						temp[count] = {
						"img_path" : os.path.join(f"{name} sprites", f"{names[count]}.png"),
						"img_size" : value["size"],
						"pos" : key
						}
						count += 1
				for stack in self.stacked:
					temp[count] = stack
					count += 1
				with open(os.path.join(path, f"{name}.json"), "w") as f:
						j.dump(temp, f, indent = True)
				self.nothing_changed = True
				self.app.show_err("File Has Been Saved.")
			except Exception as e:
				self.app.show_err("Something went wrong !")	
		else:
			self.app.showerr("Select a directory to save file !")
