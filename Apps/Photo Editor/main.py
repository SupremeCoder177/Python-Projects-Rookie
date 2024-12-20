from settings import *
from widgets import *


class App(ctk.CTk):

	def __init__(self):
		super().__init__(fg_color = APP_BG)

		app_x = (self.winfo_screenwidth() - APP_SIZE[0]) // 2
		app_y = (self.winfo_screenheight() - APP_SIZE[1]) // 2

		# window configurations
		self.title('Photo Editor')
		self.iconbitmap(ICON)
		self.geometry(f'{APP_SIZE[0]}x{APP_SIZE[1]}+{app_x}+{app_y}')
		self.minsize(int(APP_SIZE[0] * 0.75), int(APP_SIZE[1] * 0.50))
		self.maxsize(self.winfo_screenwidth(), self.winfo_screenheight())

		# layout
		self.rowconfigure(0, weight = 1, uniform = 'a')
		self.columnconfigure(0, weight = 2, uniform = 'a')
		self.columnconfigure(1, weight = 6, uniform = 'a')

		self.frame = ImageImport(self, 0, 0, APP_BG)

		self.bind('<Escape>', lambda event: self.quit())
		self.mainloop()

	def import_img(self, path):
		self.original_image = Image.open(path)
		self.image = self.original_image
		self.image_ratio = self.image.size[0] / self.image.size[1]
		self.image_tk = ImageTk.PhotoImage(self.image)
		self.frame.grid_forget()
		self.open_editor()

	def open_editor(self):
		self.editor_img = ImageCanvas(self, 0, 1)
		self.editor_panel = EditorPanel(self, 0, 0)
		self.editor_img.bind('<Configure>', self.resize_image)

	def change_img(self, *args):
		img = self.original_image

		# rotation
		rot_img = img.rotate(self.editor_panel.rot_var.get(), expand = True)

		# zoom
		zoom = self.editor_panel.zoom_var.get()
		width, height = rot_img.size
		new_width = int(width * zoom)
		new_height = int(height * zoom)
		if new_width > 0 and new_height > 0:
			img_resize = rot_img.resize((new_width, new_height))
			left = (new_width - width) // 2
			top = (new_height - height) // 2
			right = left + width
			bottom = top + height
			img_zoom = img_resize.crop((left, top, right, bottom))
			self.image = img_zoom
		else:
			self.image = rot_img

		# blur
		img_blur = self.image.filter(ImageFilter.BoxBlur(self.editor_panel.image_blur.get()))

		# filters
		brightness_enhancer = ImageEnhance.Brightness(img_blur)
		img_bright = brightness_enhancer.enhance(self.editor_panel.brightness.get())
		contrast_enhancer = ImageEnhance.Contrast(img_bright)
		img_contrast = contrast_enhancer.enhance(self.editor_panel.contrast.get())
		color_enhancer = ImageEnhance.Color(img_contrast)
		img_color = contrast_enhancer.enhance(self.editor_panel.color.get())
		sharpness_enhancer = ImageEnhance.Sharpness(img_color)
		img_sharp = sharpness_enhancer.enhance(self.editor_panel.sharpness.get())

		# flipping image
		if self.editor_panel.flip_ver.get() and self.editor_panel.flip_hor.get():
			self.image = img_sharp.transpose(Image.Transpose.TRANSPOSE)
		elif self.editor_panel.flip_ver.get():
			self.image = img_sharp.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
		elif self.editor_panel.flip_hor.get():
			self.image = self.image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
		else:
			self.image = img_sharp

		# color changes
		if self.editor_panel.invert.get():
			self.image = ImageOps.invert(self.image)
		else:
			self.image = img_sharp
		if self.editor_panel.gray_scale.get():
			self.image = ImageOps.grayscale(self.image)
		
		self.place_img(self.image)

	def reset(self):
		self.editor_img.grid_forget()
		self.editor_panel.grid_forget()
		self.frame = ImageImport(self, 0, 0, APP_BG)

	def resize_image(self, event):
		self.editor_img.delete('all')
		# resize image
		canvas_ratio = event.width / event.height

		if canvas_ratio > self.image_ratio:
			img_ht = event.height
			img_wdt = self.image_ratio * img_ht
		else:
			img_wdt = event.width
			img_ht = img_wdt / self.image_ratio

		resized_img = self.image.resize((int(img_wdt), int(img_ht)))
		self.place_img(resized_img)

	def place_img(self, img):
		self.image_tk = ImageTk.PhotoImage(img)
		self.editor_img.create_image(self.editor_img.winfo_width() / 2, self.editor_img.winfo_height() / 2, image = self.image_tk)

	def save_pic(self, *args):
		path = filedialog.asksaveasfilename(defaultextension = ".jpg",
			filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
		if path:
			self.image.save(path)

	def reset_pic(self, *args):
		self.image = self.original_image
		self.editor_panel.rot_var.set(0)
		self.editor_panel.zoom_var.set(0)
		self.editor_panel.brightness.set(1)
		self.editor_panel.color.set(1)
		self.editor_panel.contrast.set(1)
		self.editor_panel.sharpness.set(1)
		self.editor_panel.image_blur.set(0)
		self.editor_panel.flip_ver.set(False)
		self.editor_panel.flip_hor.set(False)
		self.editor_panel.invert.set(False)
		self.editor_panel.gray_scale.set(False)
		self.place_img(self.image)


if __name__ == '__main__':
	App()