# Custom Widgets

import customtkinter as ctk
from animations import Move
import time

'''
Basically a toggle frame with a slide animation
(got tired of calling it a drop down menu)

The only difference between this widget and a drop-down menu is
well, not much but you can notice it doesn't take in a end coordinate in 
horizontal or vertical direction (because it was complicated and unnecessary)
'''
class ToggleFrame(ctk.CTkFrame):

	def __init__(self, master : ctk.CTk, fg_color : str, x : float, y : float, width : float, height : float, slide_direction : str, anim_time : int):
		if slide_direction.lower() not in ["horizontal", "vertical"]: raise ValueError("slide_direction can only be vertical or horizontal")
		super().__init__(master = master, fg_color = fg_color)
		self.place(relx = x, rely = y, relwidth = width, relheight = height)
		self.start_x = x
		self.x = x
		self.start_y = y
		self.y = y
		self.at_start = True
		self.delta = 1e-3
		self.width = width
		self.height = height
		self.axis = slide_direction.lower()
		self.window = master
		self.anim_time = anim_time
		self.calculate_slide_direction()
		self.calculate_delay(anim_time)

	# calculated the end point depending on how close
	# the x or y (depending on given slide_direction) is to the borders
	# if it is too close to 0.0 then it goes towards 0.0 and same for 1.0
	def calculate_slide_direction(self):
		if self.axis == 'horizontal':
			if 1 - self.start_x < 0.5: 
				self.end = 1
			else: 
				self.end = 0 - self.width
		else:
			if 1 - self.start_y < 0.5: 
				self.end = 1
			else: 
				self.end = 0 - self.height

	# calculates the delay for each callback for animation function
	def calculate_delay(self, time):
		steps = abs(self.end - (self.start_x if self.axis == "horizontal" else self.start_y)) // self.delta
		self.delay = int(time // steps)

	def put(self):
		self.place(relx = self.x, rely = self.y, relwidth = self.width, relheight = self.height)

	def animate(self):
		if self.at_start:
			self.animate_back()
		else:
			self.animate_forward()

	def animate_back(self):
		Move().move_widget(self.window, self, self.x, self.y, self.end, self.axis, self.width, self.height, self.anim_time, self.toggle_status)

	def toggle_status(self):
		self.at_start = not self.at_start

	def animate_forward(self):
		x = self.start_x if self.axis != "horizontal" else self.end
		y = self.start_y if self.axis != "vertical" else self.end
		Move().move_widget(self.window, self, x, y, self.start_x if self.axis == "horizontal" else self.start_y, self.axis, self.width, self.height, self.anim_time, self.toggle_status)


# A clock (really can't describe it any better)
"""
Ok it will display like those digital alarm clocks with two buttons
showing the hour, minute and second,

Also the width and height arguments cannot be set because unless it
has a very specific range of width and height, it doesn't look like what
I am hoping for it to look like

Here is a real life example of what I mean
https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.amazon.in%2Fwolpin-Digital-Temperature-Display-Bedroom%2Fdp%2FB0CKXZ1TGM&psig=AOvVaw2Js_Wq6LR83naJEAAI4N-w&ust=1741224029508000&source=images&cd=vfe&opi=89978449&ved=0CBQQjRxqFwoTCNCwgZHj8YsDFQAAAAAdAAAAABAE
"""
class Clock(ctk.CTkFrame):

	def __init__(self, window : ctk.CTk, bg : str, x : float, y : float, font : ctk.CTkFont, text_clr : str, callback=lambda: None, anchor="nw"):
		super().__init__(master = window,
			fg_color = bg)
		self.width = 0.22
		self.height = 0.1
		self.x = x
		self.y = y
		self.delay = 1000 # 1 second in ms
		self.hour = ctk.StringVar(value = time.localtime().tm_hour)
		self.min = ctk.StringVar(value = time.localtime().tm_min)
		self.sec = ctk.StringVar(value = time.localtime().tm_sec)
		self.day = ctk.StringVar(value = self.week_day_map(time.localtime().tm_wday))
		self.callback = callback
		self.add_labels(font, text_clr)
		self.place(relx = self.x, rely = self.y, relwidth = self.width, relheight = self.height, anchor = anchor)
		self.next_frame()

	# a one time call function to add all the labels on the frame,
	# could've done it in the initializer, but I like to keep it clean
	def add_labels(self, font : ctk.CTkFont, clr : str) -> None:
		time_frame = ctk.CTkFrame(self, fg_color = "transparent")

		ctk.CTkLabel(self, textvariable = self.day, fg_color = "transparent",
			text_color = clr, font = font).pack(expand = True, pady = 2, padx = 2)

		ctk.CTkLabel(time_frame, textvariable = self.hour, fg_color = "transparent", text_color = clr, font = font, justify = "center").pack(side = 'left', expand = True)
		ctk.CTkLabel(time_frame, text = ":", fg_color = "transparent", text_color = clr, font = font).pack(side = 'left', padx = 2)

		ctk.CTkLabel(time_frame, textvariable = self.min, fg_color = "transparent", text_color = clr, font = font).pack(side = 'left')
		ctk.CTkLabel(time_frame, text = ":", fg_color = "transparent", text_color = clr, font = font).pack(side = 'left', padx = 2)

		ctk.CTkLabel(time_frame, textvariable = self.sec, fg_color = "transparent", text_color = clr, font = font).pack(side = 'left')

		time_frame.pack(expand = True, pady = 1)
	
	# sets new values for hour, minute, second and day variables of the clock
	def get_new_time(self) -> None:
		self.hour.set(time.localtime().tm_hour)
		self.min.set(time.localtime().tm_min)
		self.sec.set(time.localtime().tm_sec)
		self.day.set(self.week_day_map(time.localtime().tm_wday))

	# returns the week day name of the week day 
	def week_day_map(self, day : int) -> str:
		mapper = {
		1 : "Monday",
		2 : "Tuesday",
		3 : "Wednesday",
		4 : "Thrusday",
		5 : "Friday",
		6 : "Saturday",
		7 : "Sunday"
		}
		return mapper.get(day + 1, None)

	# sets new values for labels
	def next_frame(self) -> None:
		# getting new time values and setting them to the labels
		self.get_new_time()

		# finishing frame with callback
		self.callback()

		# calling again after preset delay (1 sec)
		self.after(self.delay, self.next_frame)


'''
Just a wrapper class to set the default button color and font values to a customtkinter button,
saves time nothing more than that to it
'''
class Button(ctk.CTkButton):

	def __init__(self, master : ctk.CTk, text : str, data : dict, size : int, command):
		super().__init__(master = master, fg_color = data["btn_clr"],
			hover_color = data["btn_hvr_clr"],
			text_color = data["btn_txt_clr"],
			font = ctk.CTkFont(family = data["font"], size = size),
			command = command,
			text = text)

'''
Just a label in a frame nothing too fancy,
the reason I made this widget is the fact that there is no option
to add a boder color to a label, this widget creates the illusion
of the label having a border color, though it would not
look as good if you add a corner_radius to the internal label
'''
class FrameLabel(ctk.CTkFrame):

	def __init__(self, master, text : str, bg : str, txt_clr : str, font : ctk.CTkFont, bd_clr="#eee", bd_width=0, width=100, height=50):
		super().__init__(master = master, fg_color = "transparent",
			border_color = bd_clr,
			border_width = bd_width,
			width = width,
			height = height)
		self.pack_propagate(False)
		self._label = ctk.CTkLabel(self, text = text, fg_color = bg, font = font, text_color = txt_clr)
		self._label.pack(expand = True, fill = 'both', padx = bd_width, pady = bd_width)
