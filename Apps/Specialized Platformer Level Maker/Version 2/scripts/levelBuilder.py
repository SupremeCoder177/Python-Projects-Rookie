# this module handles building the level file and its dependencies (aka sprites)

import json as j
import os
from tkinter import filedialog
from PIL import Image

class Builder:

	def __init__(self, app):
		self.app = app
		self.items = dict()
		self.placed = dict()
		self.nothing_changed = False
		self.last_save_name = None
		self.last_save_path = None

	# adds a cell to occupied
	def add_cell(self, pos):	
		self.nothing_changed = False
		img = self.app.handler.sprites[self.app.handler.curr_sprite]["sprite"]
		size = self.app.handler.sprites[self.app.handler.curr_sprite]["sprite_size"]
		if pos not in self.placed:
			self.placed[pos] = 1
		else:
			self.placed[pos] += 1
		if pos not in self.items:
			self.items[pos] = [{
				"sprite" : img,
				"size"  : size,
				"tag" : self.app.handler.curr_sprite,
				"level" : self.placed[pos]
			}]
		else:
			self.items[pos].append({
				"sprite" : img,
				"size"  : size,
				"tag" : self.app.handler.curr_sprite,
				"level" : self.placed[pos]
				})

	# adds cell data from json file
	def add_data(self, data, path):
		self.clear()
		self.last_save_name = os.path.split(path)[1].split('.')[0]
		self.last_save_path = os.path.split(path)[0]
		for item in data.values():
			for val in item.values():
				img_name = os.path.split(val["img_path"])[1]
				img_tag = [t for t in self.app.handler.sprites if os.path.split(t)[1] == img_name][0]
				img = self.app.handler.sprites[img_tag]["sprite"]
				size = self.app.handler.sprites[img_tag]["sprite_size"]
				rel_name = img_name.split('.')[0]

				if tuple(val["pos"]) not in self.placed:
					self.placed[tuple(val["pos"])] = 1
				else:
					self.placed[tuple(val["pos"])] += 1
				if tuple(val["pos"]) not in self.items:
					self.items[tuple(val["pos"])] = [{
					"sprite" : img,
					"size" : size,
					"tag" : rel_name,
					"level" : self.placed[tuple(val["pos"])]
					}]
				else:
					self.items[tuple(val["pos"])].append({
						"sprite" : img,
						"size" : size,
						"tag" : rel_name,
						"level" : self.placed[tuple(val["pos"])]
						})

	# deletes a cell from occupied 
	def delete_cell(self, pos):
		if pos in self.placed:
			self.nothing_changed = False
			for i in range(len(self.items[pos])):
				if self.items[pos][i]["level"] == self.placed[pos]:
					self.items[pos].pop(i)
					self.placed[pos] -= 1
					if self.placed[pos] < 1:
						del self.placed[pos]
						del self.items[pos]
					break

	# builds level in json form and stores all images required
	def finalize(self):
		if self.nothing_changed: return
		path = None
		if not self.last_save_path:
			path = filedialog.askdirectory()
		if path or self.last_save_path:
			name = self.app.control.file_name
			self.last_save_name = name if name else self.last_save_name
			self.last_save_path = path if path else self.last_save_path
			try:
				# making a directory to save the user images
				os.chdir(path if path else self.last_save_path)
				if f"{self.last_save_name} sprites" not in os.listdir():
					os.mkdir(f"{self.last_save_name} sprites")
				os.chdir(f"{self.last_save_name} sprites")
				invalids = ["/", ":", " ", "."]
				names = dict()
				already_saved = list()
				# saving the images inside the directory
				for value in self.items.values():
					for val in value:
						sprite_name = list()
						for ch in val["tag"]:
							if ch in invalids: continue
							else: sprite_name.append(ch)
						final_name = f"{''.join(sprite_name)}.png"
						if final_name not in already_saved:
							val["sprite"].save(final_name)
							already_saved.append(final_name)
							names[final_name] = [val["tag"]]
						else:
							names[final_name].append(val["tag"])

				# getting back to path
				os.chdir(path if path else self.last_save_path)

				# dumping the occupied cell info into a json file
				temp = dict()
				for pos in self.items:
					count = 1
					for item in self.items[pos]:
						if item["level"] == count:
							img_name = None
							for key, value in names.items():
								if item["tag"] in value: 
									img_name = key
									break
							if count not in temp:
								temp[count] = {0 : {"img_path" : os.path.join(f'{self.last_save_name} sprites', img_name), "pos" : pos}}
							else:
								length = len(temp[count])
								temp[count][length] = {"img_path" : os.path.join(f'{self.last_save_name} sprites', img_name), "pos" : pos}
							count += 1

				# writing to the json file
				with open(os.path.join(path if path else self.last_save_path, f"{self.last_save_name}.json"), "w") as f:
						j.dump(temp, f, indent = True)

				self.nothing_changed = True
				self.app.show_err("File Has Been Saved.")
			except Exception as e:
				print(e)
				self.app.show_err("Something went wrong !")	
		else:
			self.app.show_err("Select a directory to save file !")

	def clear(self):
		self.last_save_path = self.last_save_name = None
		self.items = dict()
		self.placed = dict()
		self.nothing_changed = True
