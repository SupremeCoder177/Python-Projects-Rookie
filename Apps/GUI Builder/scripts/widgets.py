# widget handling

import customtkinter as ctk
import tkinter as tk
import ttkbootstrap as ttk
from scripts.settings import *

class PlaceWidget:

	def __init__(self, app):
		self.app = app
		self.emulate_space_x = self.app.size[0] * 0.8

	def place(self, type, x, y):
		if not type in RECOG_WIDGETS: return
		if x < 0: x = 0
		if y < 0: y = 0
		if x > self.emulate_space_x: x = self.emulate_space_x
		if y > self.app.size[1]: y = self.app.size[1]

		RECOG_WIDGETS[type][self.app.curr_import](self.app,
			fg_color = self.app.curr_color).place(x = x, y = y)


class Widgets:

	def __init__(self, tab, panel):
		self.panel = panel
		self.placer = PlaceWidget(self.panel.app)
		for type in RECOG_WIDGETS.keys():
			ctk.CTkButton(tab,
				text = type,
				font = DEFAULT_FONT,
				fg_color = WIDGET_BTN_CLR,
				hover_color = WIDGET_BTN_HVR_CLR,
				command = lambda: self.set_widget(type),
				corner_radius = 10).pack(expand = True)

	def set_widget(self, type):
		self.panel.app.curr_widget = type
		self.placer.place(type, 100, 100)
		self.panel.app.customs.get_curr_customs()
		
