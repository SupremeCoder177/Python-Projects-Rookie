# Making a more useful calculator

from darkdetect import isDark
from settings import *
from widgets import *
try:
	from ctypes import windll, sizeof, c_int, byref
except:
	pass


class App(ctk.CTk):

	def __init__(self):
		super().__init__(fg_color = APP_BG)
 
		# window customizations
		self.title('')
		self.geometry(f'{APP_SIZE[0]}x{APP_SIZE[1]}')
		self.minsize(APP_SIZE[0], APP_SIZE[1])
		self.maxsize(APP_MAX_SIZE[0], APP_MAX_SIZE[1])
		self.resizable(False, False)
		self.iconbitmap(icon)
		self.chng_title_clr()
	
		# ctk.set_appearance_mode('light')

		# fonts
		self.main_font = ctk.CTkFont(family = 'Helvitica', size = MAIN_FONT_SIZE)
		self.result_label_font = ctk.CTkFont(family = 'Helvitica', size = RESULT_LABEL_FONT_SIZE)
		self.formula_label_font = ctk.CTkFont(family = 'Helvitica', size = FORMULA_LABEL_FONT_SIZE)
		self.frame = NormalLayout(self)

		# creating app dependent widgets
		self.add_widgets()

		# key binds
		self.bind('<Escape>', lambda event: self.quit())

		self.mainloop()

	def add_widgets(self):
		self.button = ctk.CTkButton(self,
			text = '>',
			font = self.main_font,
			fg_color = APP_BG,
			text_color = COLORS['label_text_color'],
			width = 20,
			height = 10,
			hover_color = BUTTON_HVR_COLOR)

		self.button.place(relx = 0.99, rely = 0.01, anchor = 'ne')

	def chng_title_clr(self):
		try:
			HWND = windll.user32.GetParent(self.winfo_id())
			ATTRIBUTE = 19
			COLOR = TITLE_COLOR
			windll.dwmapi.DwmSetWindowAttribute(HWND, ATTRIBUTE, byref(c_int(COLOR)), sizeof(c_int))
		except Exception as e:
			print(e)
			

if __name__ == '__main__':
	App()