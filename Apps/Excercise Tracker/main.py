# Making an excercise tracker 

import customtkinter as ctk
from json import load, dump
from animations import FadeAnimation
from widgets import ToggleFrame, Clock, Button, FrameLabel
from subs import BMI, BMR, Logger, BodyFatCalc
from tables import Viewer
import csv

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

		# dict to store current logged in user data
		self.user_data = {}

		# list to store current user excercise data
		self.excercise_data = []

		# excercise data field names
		self.field_names = ["Date", "Excercise Name", "Sets", "Reps/Set", "Work Volume"]
		self.field_name_type_map = {"Date" : str, "Excercise Name" : str, "Sets" : int, "Reps/Set" : int, "Work Volume" : int}

		#playing all the start animations
		self.anim_count = 0
		self.anim_index = 0
		self.make_animations()		
		# comment to skip to UI
		self.play_animations()

		# uncomment to see the UI
		#self.add_widgets()

		# testing the login UI and system
		#self.ask_login()

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
			anim_length = 1800,
			text = self.data["start_text_3"],
			text_clr = self.data["start_label_color"],
			font = ctk.CTkFont(family = self.data["font"], size = self.data["main_label_font_size"]),
			callback = self.animation_done
			),
		3 : FadeAnimation(window = self, 
			anim_length = 3500,
			text = self.data["start_text_4"],
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
			self.ask_login()
		else:
			self.anims[self.anim_index].clear()
			self.anim_index += 1
			self.play_animations()

	# logs the user out and resets global app vars
	def log_out(self):
		self.delete_ui()
		self.user_data = {}
		self.excercise_data = []
		self.ask_login()

	# asks user for login/sign up before adding main widgets to screen
	def ask_login(self):
		if hasattr(self, 'logger') and self.logger.winfo_exists():
			self.logger.destroy()
		self.logger = Logger(window = self, data = self.data, callback = self.add_widgets)

	# removes all UI when log out button is pressed
	def delete_ui(self):
		for child in self.winfo_children():
			child.destroy()

		# asking for login/sign up again 
		self.ask_login()

	# this adds all the widgets to the screen after user has logged in
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


		# button to animate option frame
		self.view = Viewer(self, self.field_names, self.data, "horizontal")

		# option frame buttons to open sub apps related to data 
		Button(self.option_frame, self.data["option_btn_text"][0], self.data, self.data["option_btn_font_size"], self.log_out).pack(expand = True)
		Button(self.option_frame, self.data["option_btn_text"][1], self.data, self.data["option_btn_font_size"], self.show_table).pack(expand = True)
		Button(self.option_frame, self.data["option_btn_text"][2], self.data, self.data["option_btn_font_size"], lambda: None).pack(expand = True)

		self.option_frame.put()
		self.option_frame.tkraise()
		self.option_btn = Button(self, "Option Menu", self.data, self.data["option_frame_toggle_btn_font_size"], self.option_frame.animate)
		self.option_btn.place(relx = 0, rely = 0, relwidth = 0.2, relheight = 0.05)
		# adding the clock at the right bottom
		self.clock = Clock(window = self, bg = self.data["clock_bg"], 
				x = self.data["clock_x"], 
				y = self.data["clock_y"], 
				font = ctk.CTkFont(family = self.data["font"], size = self.data["clock_font_size"]), 
				text_clr = self.data["clock_fg"], 
				anchor = "se")

		# a sub app useful for calculating BMI (Body Mass Index)
		# the axis argument is purely random, you can have any axis and it would still be the same
		self.bmi = BMI(self, self.data["bmi_app_x"], self.data["bmi_app_y"], self.data["sub_app_bg"], self.data["bmi_app_width"], self.data["bmi_app_height"], self.data, "horizontal")

		# a sub app useful for calculating BMR (Basal Metabolic Rate)
		self.bmr = BMR(self, self.data["bmr_app_x"], self.data["bmr_app_y"], self.data["sub_app_bg"], self.data["bmr_app_width"], self.data["bmr_app_height"], self.data, "vertical", pos_axis=False)

		# a sub app useful for calculating Body Fat Percentage
		self.bft = BodyFatCalc(self, self.data["bft_app_x"], self.data["bft_app_y"], self.data["sub_app_bg"], self.data["bft_app_width"], self.data["bft_app_height"], self.data, "horizontal", pos_axis=False)

		# button to open/close the BMI sub app
		# not using the Button class because of custom coloring
		ctk.CTkButton(self, text = "BMI", command = self.bmi.toggle_animation,
			font = ctk.CTkFont(family = self.data["font"], size = self.data["sub_apps_open_btn_font_size"]),
			fg_color = self.data["bmi_open_btn_bg"],
			hover_color = self.data["bmi_open_btn_hvr_clr"],
			text_color = self.data["bmi_open_btn_txt_clr"]).place(relx = 0, rely = 1, relwidth = 0.05, relheight = 0.05, anchor = "sw")

		# button to open/close the BMR sub app
		ctk.CTkButton(self, text = "BMR", command = self.bmr.toggle_animation,
			font = ctk.CTkFont(family = self.data["font"], size = self.data["sub_apps_open_btn_font_size"]),
			fg_color = self.data["bmr_open_btn_bg"],
			hover_color = self.data["bmr_open_btn_hvr_clr"],
			text_color = self.data["bmr_open_btn_txt_clr"]).place(relx = 0, rely = 0.94, relwidth = 0.05, relheight = 0.05, anchor = "sw")

		# button to open/close the Body Fat calculactor sub app
		ctk.CTkButton(self, text = "BFT", command = self.bft.toggle_animation,
			font = ctk.CTkFont(family = self.data["font"], size = self.data["sub_apps_open_btn_font_size"]),
			fg_color = self.data["bft_open_btn_bg"],
			hover_color = self.data["bft_open_btn_hvr_clr"],
			text_color = self.data["bft_open_btn_txt_clr"]).place(relx = 0, rely = 0.88, relwidth = 0.05, relheight = 0.05, anchor = "sw")

	def show_table(self):
		self.view.toggle_animation()
		if not self.view.shown:
			self.view.tkraise()
			self.option_frame.tkraise()
			self.option_btn.tkraise()
			self.clock.lower()
		else:
			self.bmr.tkraise()
			self.bft.tkraise()
			self.bmi.tkraise()

	# sets the user data to provided data and login or sign up according to given
	# argument, returns true if the login/sign-up was sucessful
	# loads user excercise data if sign-up or login was sucessful too
	def set_user_data(self, name : str, password : str, sign_up=False) -> bool:
		self.user_data = {"name" : name, "password" : password}
		dat = None
		with open("data/csv_mapper.json", "r") as f:
			dat = load(f)
		if sign_up:
			# returning if the user is already registered in data/csv_mapper.json
			if self.user_data["name"] in dat.keys(): return False

			# adding a new user to csv_mapper
			dat[self.user_data["name"]] = {"path" : f"data/csv/{name}.csv", "password" : self.user_data["password"]}
			with open("data/csv_mapper.json", 'w') as f:
				dump(dat, f, sort_keys = True, indent = 4)

			# making a new csv file for new user
			with open(f"data/csv/{name}.csv", 'w') as file: pass
			self.excercise_data = []
			return True
		else:
			# returning if user credentials don't match or doesn't exist
			if self.user_data["name"] not in dat.keys(): return False
			if self.user_data["password"] != dat[self.user_data["name"]]["password"]: return False
			
			# loading excercise data from csv files
			with open(dat[self.user_data["name"]]["path"], 'r', newline="") as f:
				reader = csv.DictReader(f)
				for row in reader:
					self.excercise_data.append(row)
			return True

	# adds new excercise data and uploads to csv files too
	# return true if input data was in right format
	# this function doesn't update the UI because of how the UI is structured
	# it automatically updates the next time user access the data
	def add_excercise_data(self, data : dict) -> bool:

		# checking data validity
		for field in zip(data, self.field_names):
			# checking all the field names match (which they always should but still better be safe than sorry)
			if field[0] != field[1]:
				return False

			# seeing if the data has the correct format (which again they always should be, but still better be safe than sorry)
			if not isinstance(data[field[0]], self.field_name_type_map[field[0]]): return False

		# adding data to excercise data
		self.excercise_data.append(data)

		# WARNING : The csv file that hold data should not be opened while editing the contents
		# 			or an error will be thrown and user will see a warning on UI
		name = self.user_data["name"]
		try:
			with open(f"data/csv/{name}.csv", "a", newline="") as f:
				writer = csv.DictWriter(f, fieldnames = self.field_names)
				writer.writerow(data)
		except Exception as e:
			pass
		return True


if __name__ == '__main__':
	with open("settings.json", 'r') as f:
		App(load(f))