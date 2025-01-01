# widgets

import customtkinter as ctk
from tkinter import filedialog
from settings import *

class Input(ctk.CTkFrame):

	def __init__(self, parent, path, lvl, font):
		super().__init__(master = parent, fg_color = 'transparent')

		self.path = path

		ctk.CTkLabel(self,
			text = 'Enter Path To Folder Of Maps',
			font = font,
			fg_color = LABEL_BG,
			corner_radius = 10,
			text_color = '#111').place(relx = 0.5, rely = 0.2, anchor = 'center')

		entry_path = ctk.CTkEntry(self,
			textvariable = self.path,
			font = font,
			fg_color = '#eee',
			text_color = '#111')
		entry_path.bind('<Button-1>', lambda event: self.path.set(''))
		entry_path.place(relx = 0.1, rely = 0.3, relwidth = 0.6)

		ctk.CTkButton(self,
			text = 'Browse',
			font = font,
			fg_color = BTN_BG,
			hover_color = BTN_HVR_CLR,
			command = self.ask_dir).place(relx = 0.7, rely = 0.3)

		ctk.CTkLabel(self,
			text = "Enter Level Name\n\n(If Level Does Not Exist Then One Will be created)",
			font = font,
			fg_color = LABEL_BG,
			corner_radius = 10,
			text_color = '#111').place(relx = 0.5, rely = 0.6, anchor = 'center')

		ctk.CTkEntry(self,
			font = font,
			textvariable = lvl,
			fg_color = '#eee',
			text_color = '#111').place(relx = 0.5, rely = 0.7, anchor = 'center')

		ctk.CTkButton(self,
			text = 'Load',
			font = font,
			fg_color = BTN_BG,
			hover_color = BTN_HVR_CLR,
			command = parent.load_map).place(relx = 0.5, rely = 0.8, anchor = 'center')

		self.pack(expand = True, fill = 'both')

	def ask_dir(self):
		path = filedialog.askdirectory()
		if path:
			self.path.set(path)



class EditorWidgets(ctk.CTkFrame):

	def __init__(self, parent):
		super().__init__(master = parent, fg_color = 'transparent')

		self.app = parent
		self.canvas = ctk.CTkCanvas(self, bg = 'black')
		self.view = AnimatedView(self, '#1d1f1d', 0.7, 0.95, 0.3)
		self.canvas.pack(expand = True, fill = 'both')
		self.canvas.bind('<Button-1>', self.add_rect)
		self.canvas.bind('<Button-3>', self.remove_rect)

	def zoom(self, event):
		if event.delta > 0:
			self.app.tile_size = min(100, self.app.tile_size + 1)
		if event.delta < 0:
			self.app.tile_size = max(10, self.app.tile_size - 1)
		self.refresh()

	def change_offset(self, event):
		if event.char == 'w':
			self.app.offset[1] += 10
		if event.char == 's':
			self.app.offset[1] -= 10
		if event.char == 'a':
			self.app.offset[0] += 10
		if event.char == 'd':
			self.app.offset[0] -= 10
		self.refresh()

	def get_grid_pos(self, x, y):
		return (int((x + self.app.offset[0]) / self.app.tile_size), int((y + self.app.offset[1]) / self.app.tile_size))

	def add_rect(self, event):
		pos = self.get_grid_pos(event.x, event.y)
		if pos not in self.app.rects.keys():
			self.app.rects[pos] = self.app.attributes.copy()
		self.refresh()

	def remove_rect(self, event):
		pos = self.get_grid_pos(event.x, event.y)
		if pos in self.app.rects.keys():
			del self.app.rects[pos]
		self.refresh()

	def refresh(self):
		self.canvas.delete('all')
		self.draw_rects()

	def draw_rects(self):
		for rect in self.app.rects:
			x = (rect[0] * self.app.tile_size) - self.app.offset[0]
			y = (rect[1] * self.app.tile_size) - self.app.offset[1]
			self.canvas.create_rectangle(x, y, x + self.app.tile_size, y + self.app.tile_size, fill = self.app.rects[rect]['color'])


class AnimatedView(ctk.CTkFrame):

	def __init__(self, parent, bg, start_x, end_x, width):
		super().__init__(master = parent, fg_color = bg, corner_radius = 20)
		self.x = start_x
		self.start_x = start_x
		self.end_x = end_x
		self.width = width
		self.at_start = True
		self.tabs = ctk.CTkTabview(self, fg_color = bg)
		self.tabs.add('Color')
		self.tabs.add('Attributes')
		self.tabs.add('Save')
		self.add_widgets(self.tabs.tab('Save'), parent.app.font, parent)
		Color(self.tabs.tab('Color'), parent, parent.app.font)
		Attributes(self.tabs.tab('Attributes'), parent)

		ctk.CTkButton(parent,
			text = 'x',
			font = parent.app.font,
			fg_color = 'black',
			hover_color = CLOSE_RED,
			width = 15,
			height = 15,
			corner_radius = 10,
			command = parent.app.reset).place(relx = 0.01, rely = 0.01, anchor = 'nw')

		self.columnconfigure(0, weight = 1, uniform = 'a')
		self.columnconfigure(1, weight = 8, uniform = 'a')
		self.rowconfigure(0, weight = 1, uniform = 'a')

		font = ctk.CTkFont(family = FONT, size = 50)

		self.btn = ctk.CTkButton(self,
			text = '>',
			font = font,
			fg_color = BTN_BG,
			hover_color = BTN_HVR_CLR,
			command = self.animate)

		self.btn.grid(row = 0, column = 0, sticky = 'NSEW')
		self.tabs.grid(row = 0, column = 1, sticky = 'NSEW')

		self.place(relx = start_x, rely = 0.05, relwidth = self.width, relheight = 0.9)

	def add_widgets(self, tab, font, parent):
		ctk.CTkButton(tab,
			text = "Save",
			font = font,
			corner_radius = 10,
			command = parent.app.save,
			fg_color = BTN_BG,
			hover_color = BTN_HVR_CLR).pack(expand = True)

	def animate(self):
		if self.at_start:
			self.animate_right()
		else:
			self.animate_left()

	def animate_right(self):
		if self.x < self.end_x:
			self.x += 0.01
			self.after(5, self.animate_right)
		else:
			self.at_start = False
			self.btn.configure(text = '<')
		self.place(relx = self.x, rely = 0.05, relwidth = self.width, relheight = 0.9)

	def animate_left(self):
		if self.x > self.start_x:
			self.x -= 0.01
			self.after(5, self.animate_left)
		else:
			self.at_start = True
			self.btn.configure(text = '>')
		self.place(relx = self.x, rely = 0.05, relwidth = self.width, relheight = 0.9)
		

class Color(ctk.CTkFrame):

	def __init__(self, parent, editor, font):
		super().__init__(master = parent, fg_color = 'transparent')
		self.editor = editor
		self.hex_color = self.editor.app.attributes['color']

		self.color_label = ctk.CTkLabel(self,
			text = f'Color : {self.hex_color}',
			font = font,
			fg_color = LABEL_BG,
			corner_radius = 15)
		self.color_label.pack(expand = True, pady = PADDING)

		self.string_vars = [ctk.IntVar(value = 0), ctk.IntVar(value = 0), ctk.IntVar(value = 0)]

		for i in range(3):
			ctk.CTkSlider(self,
				from_ = 0,
				to = 255,
				fg_color = '#eee',
				progress_color = '#111',
				button_color = '#333',
				button_hover_color = '#111',
				command = self.change_color,
				variable = self.string_vars[i]).pack(expand = True, pady = PADDING)

			ctk.CTkLabel(self,
				textvariable = self.string_vars[i],
				font = font,
				fg_color = LABEL_BG,
				corner_radius = 15).pack(pady = 10)

		self.pack(expand = True, fill = 'both')

	def change_color(self, var):
		red = self.string_vars[0].get()
		green = self.string_vars[1].get()
		blue = self.string_vars[2].get()
		hex_color = '#{:02x}{:02x}{:02x}'.format(red, green, blue)
		self.color_label.configure(text = f'Color : {hex_color}')
		self.editor.app.attributes['color'] = hex_color


class Attributes(ctk.CTkScrollableFrame):

	def __init__(self, parent, editor):
		super().__init__(master = parent, fg_color = 'transparent')

		self.editor = editor
		self.add_widgets()

		self.pack(expand = True, fill = 'both')

	def add_widgets(self):
		for widget in self.winfo_children():
			widget.destroy()

		for attribute in self.editor.app.attributes:
			if attribute == 'color': continue
			SingleAttribute(self, attribute, self.editor.app.attributes[attribute], self.editor)

		ctk.CTkButton(self,
			text = '+',
			font = self.editor.app.font,
			fg_color = BTN_BG,
			hover_color = BTN_HVR_CLR,
			width = 35,
			height = 35,
			command = self.add).pack(expand = True, pady = PADDING)

	def add(self):
		window = ctk.CTkToplevel()
		window.title("Input")
		window.resizable(False, False)
		window.geometry('250x200')

		new_attr = ctk.StringVar()

		ctk.CTkLabel(window,
			text = 'Enter Attribute Name',
			font = self.editor.app.font,
			fg_color = LABEL_BG,
			corner_radius = 10).pack(expand = True, pady = PADDING)

		ctk.CTkEntry(window,
			font = self.editor.app.font,
			fg_color = '#eee',
			text_color = '#111',
			textvariable = new_attr).pack(expand = True, pady = PADDING, fill = 'x')

		ctk.CTkButton(window,
			text = 'Add',
			font = self.editor.app.font,
			fg_color = BTN_BG,
			hover_color = BTN_HVR_CLR,
			command = lambda : self.add_attr(new_attr.get(), window)).pack(expand = True, pady = PADDING)

		window.bind('<Escape>', lambda event: window.destroy())
		window.mainloop()

	def add_attr(self, attr_name, window):
		if not attr_name: return
		if attr_name not in self.editor.app.attributes:
			self.editor.app.attributes[attr_name] = True
			window.destroy()
			self.add_widgets()


class SingleAttribute(ctk.CTkFrame):

	def __init__(self, parent, attr_name, attr_val, editor):
		super().__init__(master = parent, fg_color = '#2b2727')

		self.rowconfigure((0, 1), weight = 1, uniform = 'c')
		self.columnconfigure((0, 1), weight = 1, uniform = 'c')
		self.editor = editor
		self.attr_name = attr_name

		ctk.CTkLabel(self,
			font = editor.app.font,
			fg_color = LABEL_BG,
			text = attr_name).grid(row = 0, column = 0, sticky = 'NSEW')

		self.bool_var = ctk.StringVar(value = str(attr_val))
		ctk.CTkLabel(self,
			font = editor.app.font,
			fg_color = 'transparent',
			text_color = '#eee',
			textvariable = self.bool_var).grid(row = 0, column = 1, sticky = 'NSEW')

		ctk.CTkSwitch(self,
			variable = self.bool_var,
			onvalue = 'True',
			offvalue = 'False',
			command = self.change_val,
			button_color = BTN_BG,
			button_hover_color = BTN_HVR_CLR,
			font = editor.app.font,
			text = "State",
			progress_color = BTN_BG).grid(row = 1, column = 0, columnspan = 2, sticky = 'NSEW', padx = PADDING * 5)

		self.pack(expand = True, fill = 'x', pady = PADDING)

	def change_val(self):
		if self.bool_var.get() == 'True':
			self.editor.app.attributes[self.attr_name] = True
		else:
			self.editor.app.attributes[self.attr_name] = False