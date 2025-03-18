# Making an excercise tracker 

import customtkinter as ctk
from darkdetect import isDark
from json import load
from animations import FadeAnimation
from widgets import ToggleFrame, Clock, Button
from subs import BMI, BMR

# main app class
# P.S. There is no load_data function pre-built in this class unlike my other apps
#	    because I want to be able to have multiple settings for the same app
class App(ctk.CTk):

	def __init__(self, data):
		super().__init__()
		self.data = data
		self.configure(fg_color = self.data["window_bg"])

		x = (self.winfo_screenwidth() - self.data["app_size"][0]) // 2
		y = (self.winfo_screenheight() - self.data["app_size"][1]) // 2

		self.geometry(f'{self.data["app_size"][0]}x{self.data["app_size"][1]}+{x}+{y}')

		self.resizable(False, False)
		self.title(self.data["app_name"])

		#playing all the start animations
		self.anim_count = 0
		self.anim_index = 0
		self.make_animations()		
		#self.play_animations()
		self.add_widgets()

		self.bind('<Escape>', lambda event: self.quit())
		self.mainloop()

	def make_animations(self):
		self.anims = {
		0 : FadeAnimation(window = self, 
			anim_length = 2500,
			text = self.data["start_text"],
			text_clr = self.data["start_label_color"],
			font = ctk.CTkFont(family = self.data["font"], size = self.data["main_label_font_size"]),
			callback = self.animation_done
			),
		1 : FadeAnimation(window = self, 
			anim_length = 1800,
			text = self.data["start_text_2"],
			text_clr = self.data["start_label_color"],
			font = ctk.CTkFont(family = self.data["font"], size = self.data["main_label_font_size"]),
			callback = self.animation_done
			),
		2 : FadeAnimation(window = self, 
			anim_length = 3500,
			text = self.data["start_text_3"],
			text_clr = self.data["start_label_color"],
			font = ctk.CTkFont(family = self.data["font"], size = self.data["main_label_font_size"]),
			callback = self.animation_done
			)
		}
		self.anim_count = len(self.anims)

	def play_animations(self):		
		self.anims[self.anim_index].start()
		self.anims[self.anim_index].make_visible()

	def clear_animations(self):
		for anim in self.anims.values():
			anim.clear()

	def animation_done(self):
		self.anim_count -= 1
		if self.anim_count == 0:
			self.clear_animations()
			self.add_widgets()
		else:
			self.anims[self.anim_index].clear()
			self.anim_index += 1
			self.play_animations()

	def add_widgets(self):
		# main frame to toggle between logs and add frames
		self.option_frame = ToggleFrame(master = self,
			fg_color = self.data["option_frame_bg"],
			x = self.data["option_frame_x"],
			y = self.data["option_frame_y"],
			width = self.data["option_frame_width"],
			height = self.data["option_frame_height"],
			slide_direction = 'vertical',
			anim_time = 500)

		self.option_frame.put()

		# button to animate option frame
		Button(self, "Option Menu", self.data, self.data["option_frame_toggle_btn_font_size"], self.option_frame.animate).place(relx = 0, rely = 0, relwidth = 0.2, relheight = 0.05)

		# option frame buttons to open sub apps
		Button(self.option_frame, self.data["option_btn_text"][0], self.data, self.data["option_btn_font_size"], lambda: None).pack(expand = True, side = "left")
		Button(self.option_frame, self.data["option_btn_text"][1], self.data, self.data["option_btn_font_size"], lambda: None).pack(expand = True, side = "left")

		# adding the clock at the right bottom
		Clock(window = self, bg = self.data["clock_bg"], 
				x = self.data["clock_x"], 
				y = self.data["clock_y"], 
				font = ctk.CTkFont(family = self.data["font"], size = self.data["clock_font_size"]), 
				text_clr = self.data["clock_fg"], 
				anchor = "se")

		# a sub app useful for calculating BMI (Body Mass Index)
		# the axis argument is purely random, you can have any axis and it would still be the same
		bmi = BMI(self, self.data["bmi_app_x"], self.data["bmi_app_y"], self.data["sub_app_bg"], self.data["bmi_app_width"], self.data["bmi_app_height"], self.data, "horizontal")

		# a sub app useful for calculating BMR (Basal Metabolic Rate)
		bmr = BMR(self, self.data["bmr_app_x"], self.data["bmr_app_y"], self.data["sub_app_bg"], self.data["bmr_app_width"], self.data["bmr_app_height"], self.data, "vertical")

		# button to open/close the BMI sub app
		# not using the Button class because of custom coloring
		ctk.CTkButton(self, text = "BMI", command = bmi.toggle_animation,
			font = ctk.CTkFont(family = self.data["font"], size = self.data["sub_apps_open_btn_font_size"]),
			fg_color = self.data["bmi_open_btn_bg"],
			hover_color = self.data["bmi_open_btn_hvr_clr"],
			text_color = self.data["bmi_open_btn_txt_clr"]).place(relx = 0, rely = 1, relwidth = 0.05, relheight = 0.05, anchor = "sw")

		ctk.CTkButton(self, text = "BMR", command = bmr.toggle_animation,
			font = ctk.CTkFont(family = self.data["font"], size = self.data["sub_apps_open_btn_font_size"]),
			fg_color = self.data["bmr_open_btn_bg"],
			hover_color = self.data["bmr_open_btn_hvr_clr"],
			text_color = self.data["bmr_open_btn_txt_clr"]).place(relx = 0, rely = 0.94, relwidth = 0.05, relheight = 0.05, anchor = "sw")



if __name__ == '__main__':
	with open("settings.json", 'r') as f:
		App(load(f))