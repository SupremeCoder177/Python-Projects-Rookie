# widgets

import customtkinter as ctk
from json import load

data = dict()

# loading app settings from json file
def load_data():
	global data
	with open("settings.json", 'r') as f:
		data = load(f)


'''A pre-defined label for the app to use with all the right
   arguements for colors and font settings 
'''
class Label(ctk.CTkLabel):

	def __init__(self, size : int, text : str, master) -> None:
		super().__init__(master = master,
			font = (data["widget_font_family"], size),
			text_color = data["txt_clr"],
			fg_color = data["label_bg"],
			text = text,
			corner_radius = data["corner_radius"])


'''A pre defined button for the app to use,
   with all the right color and font settings
'''
class Button(ctk.CTkButton):

	def __init__(self, size : int, text : str, master, func) -> None:
		super().__init__(master = master,
			text = text,
			font = (data["widget_font_family"], size),
			text_color = data["txt_clr"],
			fg_color = data["btn_bg"],
			hover_color = data["btn_hvr_clr"],
			command = func,
			corner_radius = data["corner_radius"])


'''A pre-defined entry widget for the app to use
   with the right settings
'''
class Entry(ctk.CTkEntry):

	def __init__(self, size : int, master, textvariable) -> None:
		super().__init__(master = master,
			font = (data["user_input_font_family"], size),
			textvariable = textvariable,
			fg_color = data["entry_bg"],
			text_color = data["entry_txt_clr"],
			corner_radius = data["corner_radius"])


'''Custom label with a border color which
	gets activated when label is clicked, and also a hover color
	P.S. there is no functionality to define a border_color for a label hence I made this
	And the actual functionality is not added here, I mean for the border highlight on select
	it is implemented by the class which uses this class as widgets, it just keeps
	track of all the color settings for this particular instance
'''
class BorderLabel(ctk.CTkFrame):

	def __init__(self, master, text : str, fg_color : str, hover_color : str, border_color : str, size : int, border_width : int) -> None:
		super().__init__(master = master, fg_color = "transparent")
		self.label = ctk.CTkLabel(master = self,
			text = text,
			fg_color = fg_color,
			text_color = data["txt_clr"],
			font = (data["widget_font_family"], size))

		self.bd_clr = border_color
		self.label.bind("<Enter>", lambda _: self.label.configure(fg_color = hover_color))
		self.label.bind("<Leave>", lambda _: self.label.configure(fg_color = fg_color))
		self.pack(expand = True, fill = 'x', padx = border_width, pady = border_width)


'''Custom widget to represent
	a list as a scrollable list, with adding and 
	deletion features, and updating the UI
'''
class ListScrolledView(ctk.CTkScrollableFrame):

	def __init__(self, master) -> None:
		super().__init__(master = master, fg_color = data["list_view_bg"])
		# list of widgets which will be displayed
		self.objs = []
		# var to hold the current selected label
		self.selected_label = None

	# function to add a label to the scorlled list
	def add_label(self, text : str, size : int) -> None:
		temp = BorderLabel(self, text, data["list_view_obj_bg"], data["list_view_obj_hvr_clr"], data["list_view_obj_selection_highlight_clr"], size, data["list_view_obj_bd_width"])
		temp.label.bind("<Button-1>", lambda _: self.set_select(temp))
		self.objs.append(temp)
		self.update()

	# function to set selected label to obj and highlight it
	def set_select(self, obj) -> None:
		#unhighlighting the previous selected obj
		if self.selected_label is not None:
			self.selected_label.configure(border_color = self.cget("fg_color"))

		# setting current obj as selected
		self.selected_label = obj
		obj.configure(border_color = obj.bd_clr)

	# function to delete a label from the scorlled list
	def delete_label(self, text : str) -> None:
		temp = self.objs.copy()
		for _obj in temp:
			if _obj.label.cget("text") == text:
				self.objs.remove(_obj)
		self.update()
   
	# function to remove previous UI
	def clear(self) -> None:
		for _child in self.winfo_children():
			if _child not in self.objs:
				_child.destroy()

	# updating the UI
	def update(self) -> None:
		self.clear()
		#packing the objects in current list
		for _obj in self.objs:
			_obj.label.pack(expand = True, fill = 'both')


'''A pre-defined frame to be used for the app,
	only difference being it has a hover effect and a 
	select highlight function
'''
class HoverFrame(ctk.CTkFrame):

	def __init__(self, master):
		super().__init__(master = master,
			fg_color = data["frame_bg"],
			border_width = 4,
			border_color = data["frame_bg"])
		self.bind("<Enter>", lambda _: self.configure(fg_color = data["frame_hvr_clr"], border_color = data["frame_select_highlight_clr"]))
		self.bind("<Leave>", lambda _: self.configure(fg_color = data["frame_bg"], border_color = data["frame_bg"]))



# making sure data is only loaded when file is run as a lib
if __name__ != "__main__":
	load_data()

