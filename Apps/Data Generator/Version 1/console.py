# this class handles the console which displays the app status to the user

import customtkinter as ctk


class Console(ctk.CTkFrame):

	def __init__(self, master : ctk.CTk, settings : dict):
		super().__init__(master = master)
		self.settings = settings

		self.default_messages = {
		"default" : "App status, good !",
		"error" : "An error has occurred,\nplease exit the application\nand try again.",
		"warning" : "Input error has occurred"
		}

		self.display_label = ctk.CTkTextbox(self,
			text_color = self.settings["console_txt_clr"],
			fg_color = "transparent",
			state = "disabled")
		self.change_text(self.default_messages["default"])

		self.display_label.place(relx = 0.1, rely = 0.1, relwidth = 0.8, relheight = 0.8)
		self.configure(fg_color = self.settings["console_bg"])
		self.place(relx = self.settings["console_pos"][0], rely = self.settings["console_pos"][1], relwidth = self.settings["console_dimensions"][0], relheight = self.settings["console_dimensions"][1])

	# sets the text of the display label to the input text argument for the given amount of time in milliseconds, 
	# and then sets the text to the after_msg argument provided
	def set_text(self, text : str, time : int, after_msg : str) -> None:
		self.change_text(text)
		self.master.after(time, lambda: self.change_text(after_msg))

	# changes the text in the display label
	def change_text(self, text : str) -> None:
		self.display_label.configure(state = "normal")
		self.display_label.delete("0.0", "end")
		self.display_label.insert("0.0", text)
		self.display_label.configure(state = "disabled")

	# sets the text in the display label to the error message
	def display_error(self) -> None:
		self.set_text(self.default_messages["error"], 2000, "")

	# sets the text in the display label to the warning message
	def display_warning(self) -> None:
		self.set_text(self.default_messages["warning"], 2000, "")
