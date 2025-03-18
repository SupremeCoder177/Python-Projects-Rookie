# sub apps 
# this file holds all the frames with the sub apps that the main app uses

# Also just a note to me, there is no need to make any of these too fancy (because they are sub apps)

import customtkinter as ctk
from animations import Move
from widgets import *

'''
Template class to define every sub app in this file
Uses Move class from animations.py to animate its movement
'''
class Subs(ctk.CTkFrame):

	def __init__(self, master : ctk.CTk, x : float, y : float, bg : str, width : float, height : float, axis : str, shown=False, time=300, pos_axis=True):
		super().__init__(master = master, fg_color = bg)
		
		self.shown = shown
		self.time = time
		self.start = x if axis == "horizontal" else y
		self.end = 1 if pos_axis else 0 - (width if axis == "horizontal" else height)

		# initilizing starting coordinates on whether app is shown or not
		if not shown:
			self.x = self.end if axis == "horizontal" else x
			self.y = self.end if axis == "vertical" else y
		else:
			self.x = x
			self.y = y

		self.start_x = x
		self.start_y = y
		self.axis = axis
		self.widget_width = width
		self.widget_height = height
		self.anim_started = False

	# function to trigger animation
	def toggle_animation(self):
		if self.anim_started: return
		self.anim_started = True
		end = self.start if not self.shown else self.end
		Move().move_widget(window = self.master, widget = self, x = self.x, y = self.y, end = end, axis = self.axis, width = self.widget_width, height = self.widget_height, time = self.time, callback = self.anim_callback)

	# changes the x, y and shown vars after animation completion
	# reason they are not changed by the Move class is because they are passed
	# as just values not pointers
	def anim_callback(self):
		self.anim_started = False
		self.shown = not self.shown
		if self.shown:
			self.x = self.start_x
			self.y = self.start_y
		else:
			self.x = self.end if self.axis == "horizontal" else self.start_x
			self.y = self.end if self.axis == "vertical" else self.start_y


'''
A sub app to calculate bmi
'''
class BMI(Subs):

	def __init__(self, master : ctk.CTk, x : float, y : float, bg : str, width : float, height : float, data : dict, axis : str, shown=False, time=300, pos_axis=True):
		super().__init__(master, x, y, bg, width, height, axis, shown = shown, time = time, pos_axis = pos_axis)
		self.configure(border_color = data["sub_app_bd_clr"], border_width = data["sub_app_bd_width"])
		
		self.add_widgets(data)
		self.place(relx = self.x, rely = self.y, relwidth = width, relheight = height)

	# adds widget to the frame, one time call function, never call again
	def add_widgets(self, data):
		self.rowconfigure(0, weight = 2, uniform = 'a')
		self.rowconfigure(1, weight = 4, uniform = 'a')
		self.rowconfigure(2, weight = 1, uniform = 'a')
		self.rowconfigure(3, weight = 2, uniform = 'a')
		self.columnconfigure((0, 1), weight = 1, uniform = 'a')

		self.height = ctk.StringVar(value = "0.0")
		self.weight = ctk.StringVar(value = "0.0")

		ctk.CTkLabel(self, text = "Calculate BMI",
			font = ctk.CTkFont(data["font"], size = data["bmi_font_size"]),
			fg_color = data["bmi_label_bg"],
			text_color = data["bmi_label_txt_clr"],
			corner_radius = 15).grid(row = 0, column = 0, columnspan = 2, sticky = 'NSEW', padx = data["sub_app_bd_width"] * 5, pady = data["sub_app_bd_width"] * 2)

		height_frame = ctk.CTkFrame(self, fg_color = "transparent")

		ctk.CTkLabel(height_frame, text = "Enter Height(cm)",
			font = ctk.CTkFont(family = data["font"], size = data["bmi_input_font_size"]),
			fg_color = data["bmi_label_bg"],
			text_color = data["bmi_label_txt_clr"],
			corner_radius = 10).pack(expand = True)

		ctk.CTkEntry(height_frame,
			textvariable = self.height).pack(expand = True, fill = 'x')

		height_frame.grid(row = 1, column = 0, sticky = "NSEW", padx = data["sub_app_bd_width"])

		weight_frame = ctk.CTkFrame(self, fg_color = "transparent")

		ctk.CTkLabel(weight_frame, text = "Enter Weight(kg)",
			font = ctk.CTkFont(family = data["font"], size = data["bmi_input_font_size"]),
			fg_color = data["bmi_label_bg"],
			text_color = data["bmi_label_txt_clr"],
			corner_radius = 10).pack(expand = True)

		ctk.CTkEntry(weight_frame,
			textvariable = self.weight).pack(expand = True, fill = 'x')

		weight_frame.grid(row = 1, column = 1, sticky = "NSEW", padx = data["sub_app_bd_width"])

		ctk.CTkButton(self, text = "Calculate", 
			font = ctk.CTkFont(family = data["font"], size = data["bmi_font_size"]),
			text_color = data["bmi_btn_txt_clr"],
			fg_color = data["bmi_btn_bg"],
			hover_color = data["bmi_btn_hvr_clr"],
			corner_radius = 15,
			command = self.calculate).grid(row = 2, column = 0, columnspan = 2)

		self.display_label = ctk.CTkLabel(self,
			fg_color = "transparent",
			text_color = "#eee",
			font = ctk.CTkFont(family = data["font"], size = data["bmi_font_size"]),
			text = "")
		
		self.display_label.grid(row = 3, column = 0, columnspan = 2, sticky = "NSEW", padx = data["sub_app_bd_width"], pady = data["sub_app_bd_width"])

	# calculates bmi and displays on the display label,
	# also shows appropriate errors when user enters incorrect data in entry fields
	def calculate(self):
		try:
			height = float(self.height.get())
			weight = float(self.weight.get())
			bmi = None
			if height == 0:
				self.display("Invalid Weight !!", 1500)
				return
			elif height < 0 or weight < 0:
				self.display("Ht/Wt less than 0!!", 1500)
				return
			else:
				bmi = weight / ((height / 100) ** 2)
			self.display(bmi, 2000)
		except ValueError:
			self.display("Invalid Input !!", 1500)

	# displays text on display label for given amount of time
	def display(self, text : str, time : int):
	    self.display_label.configure(text = text)
	    
	    if not self.display_label.winfo_ismapped():
	        self.display_label.grid(row = 3, column = 0, columnspan = 2, sticky = "NSEW", padx = 2, pady = 2)

	    self.master.after(time, self.display_label.grid_forget)


'''
Sub app to calculate the BMR
'''
class BMR(Subs):

	def __init__(self, master : ctk.CTk, x : float, y : float, bg : str, width : float, height : float, data : dict, axis : str, shown=False, time=300, pos_axis=True):
		super().__init__(master, x, y, bg, width, height, axis, shown = shown, time = time, pos_axis = pos_axis)
		self.configure(border_color = data["sub_app_bd_clr"], border_width = data["sub_app_bd_width"])

		self.add_widgets(data)
		self.place(relx = self.x, rely = self.y, relwidth = width, relheight = height)

	# adds widgets to the sub app, one time call function
	def add_widgets(self, data):
		self.rowconfigure(0, weight = 2, uniform = 'a')
		self.rowconfigure(1, weight = 1, uniform = 'a')
		self.rowconfigure(2, weight = 3, uniform = 'a')
		self.rowconfigure(3, weight = 2, uniform = 'a')
		self.columnconfigure(0, weight = 1, uniform = 'a')

		self.age = ctk.IntVar(value = 1)
		self.gender = ctk.StringVar(value = "male")
		self.height = ctk.StringVar(value = 0)
		self.weight = ctk.StringVar(value = 0.0)

		slide_frame = ctk.CTkFrame(self, fg_color = "transparent")

		ctk.CTkLabel(slide_frame,
			text = "Choose Age",
			font = ctk.CTkFont(family = data["font"], size = data["bmr_age_input_font_size"]),
			fg_color = "transparent",
			text_color = "#eee").pack(expand = True)

		ctk.CTkSlider(slide_frame,
			from_ = 1,
			to = 100,
			button_color = data["bmr_slider_bg_clr"],
			button_hover_color = data["bmr_slider_hvr_clr"],
			progress_color = data["bmr_slider_slide_clr"],
			variable = self.age,
			height = 10).pack(expand = True, side = 'left')

		ctk.CTkLabel(slide_frame,
			textvariable = self.age,
			font = ctk.CTkFont(family = data["font"], size = data["bmr_age_input_font_size"]),
			fg_color = "transparent",
			text_color = "#eee").pack(side = 'left', padx = data["sub_app_bd_width"] * 2, expand = True)

		gender_frame = ctk.CTkFrame(self, fg_color = "transparent")

		ctk.CTkCheckBox(gender_frame,
			text = "Male",
			font = ctk.CTkFont(family = data["font"], size = data["bmr_gender_input_font_size"]),
			onvalue = "male",
			offvalue = "female",
			variable = self.gender,
			checkbox_width = data["bmr_gender_input_font_size"],
			checkbox_height = data["bmr_gender_input_font_size"],
			hover = True,
			fg_color = data["bmr_radio_btn_bg"],
			hover_color = data["bmr_radio_btn_hvr_clr"]).pack(expand = True, side = "left")

		ctk.CTkCheckBox(gender_frame,
			text = "Female",
			font = ctk.CTkFont(family = data["font"], size = data["bmr_gender_input_font_size"]),
			onvalue = "female",
			offvalue = "male",
			variable = self.gender,
			checkbox_width = data["bmr_gender_input_font_size"],
			checkbox_height = data["bmr_gender_input_font_size"],
			hover = True,
			fg_color = data["bmr_radio_btn_bg"],
			hover_color = data["bmr_radio_btn_hvr_clr"]).pack(expand = True, side = "left")

		stats_frame = ctk.CTkFrame(self, fg_color = "transparent")

		ctk.CTkLabel(stats_frame,
			text = "Height (cm)",
			font = ctk.CTkFont(family = data["font"], size = data["bmr_stats_input_font_size"]),
			fg_color = data["bmr_label_bg"],
			text_color = data["bmr_label_txt_clr"],
			corner_radius = 15,
			height = data["bmr_stats_input_font_size"] + 2).pack(expand = True, pady = data["sub_app_bd_width"] * 2)

		ctk.CTkEntry(stats_frame,
			textvariable = self.height,
			height = 10).pack(expand = True, fill = 'x')

		ctk.CTkLabel(stats_frame,
			text = "Weight (kg)",
			font = ctk.CTkFont(family = data["font"], size = data["bmr_stats_input_font_size"]),
			fg_color = data["bmr_label_bg"],
			text_color = data["bmr_label_txt_clr"],
			corner_radius = 15,
			height = data["bmr_stats_input_font_size"] + 2).pack(expand = True, pady = data["sub_app_bd_width"] * 2)

		ctk.CTkEntry(stats_frame,
			textvariable = self.weight,
			height = 10).pack(expand = True, fill = 'x')

		calc_frame = ctk.CTkFrame(self,
			fg_color = "transparent")

		calc_frame.rowconfigure(0, weight = 1, uniform = 'b')
		calc_frame.columnconfigure(0, weight = 2, uniform = 'b')
		calc_frame.columnconfigure(1, weight = 3, uniform = 'b')

		ctk.CTkButton(calc_frame,
			text = "Calculate BMR",
			font = ctk.CTkFont(family = data["font"], size = data["bmr_font_size"]),
			fg_color = data["bmr_calc_btn_bg"],
			hover_color = data["bmr_calc_btn_hvr_clr"],
			text_color = data["bmr_calc_btn_txt_clr"],
			command = self.calculate).grid(row = 0, column = 0)

		self.display_label = ctk.CTkLabel(calc_frame,
			text = "",
			fg_color = "transparent",
			text_color = "#eee",
			font = ctk.CTkFont(family = data["font"], size = data["bmr_display_label_font_size"]))
		self.display_label.grid(row = 0, column = 1, sticky = "NSEW")

		slide_frame.grid(row = 0, column = 0, sticky = "NSEW", padx = data["sub_app_bd_width"], pady = data["sub_app_bd_width"])
		gender_frame.grid(row = 1, column = 0, sticky = "NSEW", padx = data["sub_app_bd_width"])
		stats_frame.grid(row = 2, column = 0, sticky = "NSEW", padx = data["sub_app_bd_width"])
		calc_frame.grid(row = 3, column = 0, sticky = "NSEW", padx = data["sub_app_bd_width"], pady = data["sub_app_bd_width"])

	# calculate the bmr and display it on the display label
	# also checks for incorrect input and displays the appropriate warning on the
	# display label
	def calculate(self):
		wt = ht = None
		try:
			wt = float(self.weight.get())		
			ht = int(self.height.get())
		except ValueError:
			self.display("Invalid wt/ht !", 1500)
			return

		# checking it weight or height is less than 0 or equal to 0
		if wt <= 0 or ht <= 0:
			self.display("wt/ht need to be\npositive", 1500)
			return

		# calculating bmr based on gender according to the Harris-Benedict equation or the Mifflin-St. Jeor equation
		if self.gender.get() == "male":
			output = 88.362 + (13.397 * wt) + (4.799 * ht) - (5.677 * self.age.get())
		else:
			output = 447.593 + (9.247 * wt) + (3.098 * ht) - (4.330 * self.age.get())

		# rounding the output to 3 decimal digits
		output = round(output, 3)

		# displaying the output
		self.display(output, 2000)

	# function to display given text on the display label for the given amount of time
	def display(self, text : str, time : int):
		self.display_label.configure(text = text)

		if not self.display_label.winfo_ismapped():
			self.display_label.grid(row = 0, column = 1, sticky = "NSEW")

		self.master.after(time, self.display_label.grid_forget)
