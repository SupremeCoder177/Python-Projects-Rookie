from settings import *
from tkinter import filedialog, Canvas

class ImageImport(ctk.CTkFrame):

	def __init__(self, parent, row, col, background):
		super().__init__(master = parent, fg_color = background)

		ctk.CTkButton(self,
			text = 'Import Image',
			command = lambda : self.import_img(parent),
			fg_color = BTN_COLOR,
			hover_color = BTN_HVR_CLR).pack(expand = True)

		self.grid(row = row, column = col, columnspan = 2, sticky = 'NSEW')

	def import_img(self, parent):
		path = filedialog.askopenfile()
		if path:
			path_name = path.name
			parent.import_img(path_name)


class ImageCanvas(Canvas):

	def __init__(self, parent, row, col):
		super().__init__(master = parent, bd = 0, highlightthickness = 0, relief = 'ridge', background = APP_BG[1] if is_dark else APP_BG[0])

		ctk.CTkButton(self, text = 'x', fg_color = CLOSE_FG, hover_color = CLOSE_RED, width = 30, height = 25, command = parent.reset).place(relx = 0.99, rely = 0.0, anchor = 'ne')

		self.grid(row = row, column = col, sticky = 'NSEW', padx = PADDING, pady = PADDING)


class EditorPanel(ctk.CTkTabview):

	def __init__(self, parent, row, col):
		super().__init__(master = parent, fg_color = PANEL_BG, corner_radius = PANEL_CORNER_RADIUS)

		# vars
		self.rot_var = ctk.DoubleVar(value = 0)
		self.zoom_var = ctk.DoubleVar(value = 0)
		self.brightness = ctk.DoubleVar(value = 1)
		self.contrast = ctk.DoubleVar(value = 1)
		self.color = ctk.DoubleVar(value = 1)
		self.sharpness = ctk.DoubleVar(value = 1)
		self.image_blur = ctk.DoubleVar(value = 0)
		self.flip_ver = ctk.BooleanVar(value = False)
		self.flip_hor = ctk.BooleanVar(value = False)
		self.save = ctk.BooleanVar(value = False)
		self.reset = ctk.BooleanVar(value = False)
		self.invert = ctk.BooleanVar(value = False)
		self.gray_scale = ctk.BooleanVar(value = False)
		self.parent = parent

		# trace
		self.rot_var.trace('w', parent.change_img)
		self.zoom_var.trace('w', parent.change_img)
		self.brightness.trace('w', parent.change_img)
		self.contrast.trace('w', parent.change_img)
		self.color.trace('w', parent.change_img)
		self.sharpness.trace('w', parent.change_img)
		self.image_blur.trace('w', parent.change_img)
		self.save.trace('w', parent.save_pic)
		self.flip_ver.trace('w', parent.change_img)
		self.flip_hor.trace('w', parent.change_img)
		self.reset.trace('w', parent.reset_pic)
		self.invert.trace('w', parent.change_img)
		self.gray_scale.trace('w', parent.change_img)

		# tabs
		self.add('Appearance')
		self.add('Color')
		self.add('Filters')
		self.add('Save')

		self.add_widgets()

		self.grid(row = row, column = col, sticky = 'NSEW', padx = PADDING, pady = PADDING)

	def add_widgets(self):
		Appearance(self.tab('Appearance'), PANEL_BG, self.rot_var, self.zoom_var, self.image_blur, self.reset, self.flip_ver, self.flip_hor)
		Filters(self.tab('Filters'), PANEL_BG, self.brightness, self.contrast, self.color, self.sharpness)
		Save(self.tab('Save'), PANEL_BG, self.save)
		Color(self.tab('Color'), PANEL_BG, self.invert, self.gray_scale)


class Appearance(ctk.CTkFrame):

	def __init__(self, parent, bg, *args):
		super().__init__(master = parent, fg_color = bg)

		self.rot_var = args[0]
		self.zoom_var = args[1]
		self.blur = args[2]
		self.reset = args[3]
		self.flip_ver = args[4]
		self.flip_hor = args[5]
		self.add_widgets()

		self.pack(expand = True, fill = 'both')

	def add_widgets(self):
		self.label_font = ctk.CTkFont(family = FONT, size = LABEL_FONT_SIZE)
		SliderPanel(parent = self, 
			text = 'Rotation', 
			font = self.label_font,
			var = self.rot_var, 
			min_val = 0, 
			max_val = 360)
		SliderPanel(parent = self, 
			text = 'Zoom', 
			font = self.label_font, 
			var = self.zoom_var, 
			min_val = 0, 
			max_val = 5)
		SliderPanel(parent = self, 
			text = 'Blur', 
			font = self.label_font, 
			var = self.blur, 
			min_val = 0, 
			max_val = 5)

		OptionFrame(self,
			{'text' : 'X', 'var' : self.flip_hor},
			{'text' : 'Y', 'var' : self.flip_ver})

		ctk.CTkButton(self,
			text = 'Reset',
			font = self.label_font,
			fg_color = BTN_COLOR,
			hover_color = BTN_HVR_CLR,
			command = lambda: self.reset.set(not self.reset.get())).pack(expand = True)


class OptionFrame(ctk.CTkFrame):

	def __init__(self, parent, *args):
		super().__init__(master = parent, fg_color = OPTION_FRAME_BG)

		self.pack_propagate(True)
		self.args = args
		self.add_widgets()

		self.pack(fill = 'x', padx = PADDING, pady = PADDING)

	def add_widgets(self):
		for arg in self.args:
			ctk.CTkButton(self,
				text = arg['text'],
				command = lambda var=arg['var']: var.set(not var.get()),
				fg_color = 'transparent',
				hover_color = OPTION_FRAME_BTN_HVR_CLR).pack(expand = True, side = 'left', padx = PADDING, pady = PADDING, fill = 'x')


class Filters(ctk.CTkFrame):

	def __init__(self, parent, bg, *args):
		super().__init__(master = parent, fg_color = bg)

		# vars
		self.brightness = args[0]
		self.contrast = args[1]
		self.color = args[2]
		self.sharpness = args[3]

		self.add_widgets()

		self.pack(expand = True, fill = 'both')

	def add_widgets(self):
		self.label_font = ctk.CTkFont(family = FONT, size = LABEL_FONT_SIZE)
		SliderPanel(parent = self,
			text = 'Brightness',
			font = self.label_font,
			var = self.brightness,
			min_val = 0,
			max_val = 5)
		SliderPanel(parent = self,
			text = 'Contrast',
			font = self.label_font,
			var = self.contrast,
			min_val = 0,
			max_val = 5)
		SliderPanel(parent = self,
			text = 'Color',
			font = self.label_font,
			var = self.color,
			min_val = 0,
			max_val = 5)
		SliderPanel(parent = self,
			text = 'Sharpness',
			font = self.label_font,
			var = self.sharpness,
			min_val = 0,
			max_val = 5)


class Save(ctk.CTkFrame):

	def __init__(self, parent, bg, save):
		super().__init__(master = parent, fg_color = bg)

		self.add_widgets()
		self.save = save

		self.pack(expand = True, fill = 'both')

	def add_widgets(self):
		frame = ctk.CTkFrame(self, fg_color = PANEL_WIDGET_BG)

		self.path = ctk.StringVar(value = '')
		self.file_name = ctk.StringVar(value = 'image')
		
		ctk.CTkButton(frame, text = 'Save', font = ("Cascasia Mono", 10), command = self.save_pic, fg_color = SAVE_BTN_COLOR, hover_color = SAVE_BTN_HVR_CLR).pack(expand = True, pady = PADDING, padx = PADDING)

		frame.pack(expand = True, fill = 'both')

	def ask_path(self):
		path = filedialog.askdirectory(title = 'Select A Folder')
		if path:
			self.path.set(path)

	def save_pic(self):
		self.save.set(not self.save.get())


class Color(ctk.CTkFrame):

	def __init__(self, parent, bg, *args):
		super().__init__(master = parent, fg_color = bg)

		self.invert = args[0]
		self.gray_scale = args[1]

		self.add_widgets()

		self.pack(expand = True, fill = 'both', padx = PADDING, pady = PADDING)

	def add_widgets(self):
		OptionFrame(self,
			{'text' : 'Invert', 'var' : self.invert},
			{'text' : 'GrayScale', 'var' : self.gray_scale})

class SliderPanel(ctk.CTkFrame):

	def __init__(self, parent, text, font, var, min_val, max_val):
		super().__init__(master = parent, fg_color = PANEL_WIDGET_BG)
		self.rowconfigure((0, 1), weight = 1, uniform = 'a')
		self.columnconfigure((0, 1), weight = 1, uniform = 'a')

		ctk.CTkLabel(self, text = text,
			font = font,
			text_color = TEXT_COLOR).grid(row = 0, column = 0, padx = 3, pady = 3, sticky = 'W')

		self.label = ctk.CTkLabel(self, text = var.get())
		self.label.grid(row = 0 , column = 1, sticky = 'E', padx = 3, pady = 3)

		ctk.CTkSlider(self,
			fg_color = SLIDER_BG,
			from_ = min_val,
			to = max_val,
			variable = var,
			command = self.change_text).grid(row = 1, column = 0, columnspan = 2, sticky = 'NSEW', padx = 3, pady = 3)		

		self.pack(fill = 'x', padx = PADDING, pady = PADDING)

	def change_text(self, event):
		self.label.configure(text = round(event, 2))