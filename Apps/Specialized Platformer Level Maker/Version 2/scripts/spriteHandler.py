# this module handles all the loading and unloading of sprites from images

from PIL import Image


class SpriteHandler:

	def __init__(self, master):
		self.show_err = master.show_err
		self.cell_size = master.settings["cell_size"]
		self.min_size = master.settings["min_cell_size"]
		self.sprites = dict()
		self.final_sprites = dict()
		self.curr_sprite = None

	def get_sprites(self, path : str):
		img = None
		try:
			img = Image.open(path)
			for i in range(img.size[0] // self.cell_size):
				for j in range(img.size[1] // self.cell_size):
					if f'{path}{i}{j}{self.cell_size}' in self.sprites: continue
					temp = img.crop((i * self.cell_size, j * self.cell_size, (i + 1) * self.cell_size, (j + 1) * self.cell_size))
					self.sprites[f'{path}{i}{j}{self.cell_size}'] = {
					"sprite" : temp,
					"sprite_size" : (self.cell_size, self.cell_size),
					}
		except Exception as e:
			self.show_err("The chosen file cannot be read !!")
			self.show_err("Either lower cell size or choose another file.")

	def change_cell_size(self, new_size):
		if new_size < self.min_size:
			self.show_err("Cell Size Cannot be less than 10 !")
			return False
		self.cell_size = new_size
		return True

	def set_current_sprite(self, tag):
		self.curr_sprite = tag if tag in self.sprites else self.curr_sprite

	def delete_sprite(self):
		if not self.curr_sprite: return
		del self.sprites[self.curr_sprite]

	def delete_all(self):
		self.sprites = dict()
		self.curr_sprite = None

	def add_finals(self, sprite):
		pass

	def get_cell_size(self):
		return self.cell_size