# Control Panel

import customtkinter as ctk
from scripts.usables import *
from scripts.settings import *
from scripts.widgets import *

class Panel(ctk.CTkTabview):
	def __init__(self, parent):
		super().__init__(master = parent, fg_color = 'transparent')
		self.add('Size')
		self.add('Widegts')
		self.add('Imports')
		self.add('Vars')
		self.app = parent
		self.app.rowconfigure(0, weight = 1, uniform = 'a')
		self.app.columnconfigure(0, weight = 4, uniform = 'a')
		self.app.columnconfigure(1, weight = 1, uniform = 'a')
		self.grid(row = 0, column = 1, sticky = 'NSEW')
		self.add_widgets()

	def add_widgets(self):
		Size(self.tab('Size'), self)
		Imports(self.tab('Imports'), self)
		Widgets(self.tab('Widegts'), self)

class Size:

	def __init__(self, tab, panel):
		self.panel = panel
		app_size_frame = ctk.CTkFrame(tab,
			fg_color = '#222')
		ctk.CTkLabel(app_size_frame,
			text = 'Change App Size',
			fg_color = 'transparent',
			font = SLIDER_FRAME_FONT).pack(pady = 10)
		tab.rowconfigure((0, 1), weight = 1, uniform = 'c')
		tab.columnconfigure(0, weight = 1, uniform = 'c')
		SliderFrame(app_size_frame, SLIDER_FRAME_CLR, 100, 1000, SLIDER_FRAME_BTN_CLR, SLIDER_FRAME_BTN_HVR_CLR, SLIDER_FRAME_PROGRESS_CLR, SLIDER_FRAME_FONT, self.panel.app.emulate_app_size_x, 'X : ').pack(expand = True, padx = 10)
		SliderFrame(app_size_frame, SLIDER_FRAME_CLR, 100, 1000, SLIDER_FRAME_BTN_CLR, SLIDER_FRAME_BTN_HVR_CLR, SLIDER_FRAME_PROGRESS_CLR, SLIDER_FRAME_FONT, self.panel.app.emulate_app_size_y, 'Y : ').pack(expand = True, padx = 10)
		app_size_frame.grid(row = 0, column = 0, sticky = 'NSEW')

		widget_size_frame = ctk.CTkFrame(tab,
			fg_color = '#333')
		ctk.CTkLabel(widget_size_frame,
			text = 'Change Selected\nWidget Size',
			font = SLIDER_FRAME_FONT,
			fg_color = 'transparent').pack(pady = 10)
		SliderFrame(widget_size_frame, SLIDER_FRAME_CLR, 10, 1000, SLIDER_FRAME_BTN_CLR, SLIDER_FRAME_BTN_HVR_CLR, SLIDER_FRAME_PROGRESS_CLR, SLIDER_FRAME_FONT, self.panel.app.widget_size_x, 'X : ').pack(expand = True, padx = 10)
		SliderFrame(widget_size_frame, SLIDER_FRAME_CLR, 10, 1000, SLIDER_FRAME_BTN_CLR, SLIDER_FRAME_BTN_HVR_CLR, SLIDER_FRAME_PROGRESS_CLR, SLIDER_FRAME_FONT, self.panel.app.widget_size_y, 'Y : ').pack(expand = True, padx = 10)
		widget_size_frame.grid(row = 1, column = 0, sticky = 'NSEW')


class Imports:

	def __init__(self, tab, panel):
		self.panel = panel
		self.label = ctk.CTkLabel(tab,
			text = f'Current Import :\n{self.panel.app.curr_import}',
			font = DEFAULT_FONT,
			fg_color = 'transparent')
		self.label.pack(pady = 10)

		ctk.CTkButton(tab,
			text = 'Tkinter',
			fg_color = DEFAULT_BTN_CLR,
			hover_color = DEFAULT_BTN_HVR_CLR,
			command = lambda: self.change_import('tkinter'),
			font = DEFAULT_FONT,
			corner_radius = 10).pack(expand = True)
		ctk.CTkButton(tab,
			text = 'Custom Tkinter',
			fg_color = DEFAULT_BTN_CLR,
			hover_color = DEFAULT_BTN_HVR_CLR,
			command = lambda: self.change_import('customtkinter'),
			font = DEFAULT_FONT,
			corner_radius = 10).pack(expand = True)
		ctk.CTkButton(tab,
			text = 'Ttkbootstrap',
			fg_color = DEFAULT_BTN_CLR,
			hover_color = DEFAULT_BTN_HVR_CLR,
			command = lambda: self.change_import('ttkbootstrap'),
			font = DEFAULT_FONT,
			corner_radius = 10).pack(expand = True)

	def change_import(self, import_name):
		self.panel.app.curr_import = import_name
		self.label.configure(text = f'Current Import :\n{import_name}')