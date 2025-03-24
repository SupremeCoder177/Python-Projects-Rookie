# making UI animations

import customtkinter as ctk


def convert_to_hex(num):
	output = ""
	mapper = {
	0 : "0",
	1 : "1",
	2 : "2",
	3 : "3",
	4 : "4",
	5 : "5",
	6 : "6",
	7 : "7",
	8 : "8",
	9 : "9",
	10 : "A",
	11 : "B",
	12 : "C",
	13 : "D",
	14 : "E",
	15 : "F"
	}
	while True:
		temp = num % 16
		output += mapper[temp]
		num = num // 16
		if num == 0: break
	return "".join(list(reversed(output)))


def convert_to_int(_hex):
	output = 0
	mapper = {
	"0" : 0,
	"1" : 1,
	"2" : 2,
	"3" : 3,
	"4" : 4,
	"5" : 5,
	"6" : 6,
	"7" : 7,
	"8" : 8,
	"9" : 9,
	"A" : 10,
	"B" : 11,
	"C" : 12,
	"D" : 13,
	"E" : 14,
	"F" : 15
	}
	for i in range(len(_hex)):
		output += (16 ** i) * mapper[_hex[len(_hex) - 1 - i].upper()]
	return output


def stepper(start, end, steps):
	return abs(start - end) // steps


def convert_clr_int(clr):
	if len(clr) > 7: raise ValueError("Wrong colour values .")
	temp = []
	if len(clr) > 4:
		for i in range(1, len(clr), 2):
			temp.append(f"{clr[i]}{clr[i + 1]}")
	else:
		for i in range(1, len(clr)):
			temp.append(clr[i])
	output = []
	for val in temp:
		if len(val) > 1:
			output.append(convert_to_int(val))
		else:
			output.append(convert_to_int(f"{val}{val}"))
	return output


def convert_clr_hex(clr):
	output = []
	for val in clr:
		output.append(convert_to_hex(val))
	for i in range(len(output)):
		if len(output[i]) < 2:
			temp = output[i]
			output[i] = f'0{temp}'
	return f'#{"".join(output)}'


def get_clr_diff(clr1, clr2):
	output = 0
	for i in range(len(clr1)):
		output += abs(clr1[i] - clr2[i])
	return output / len(clr1)


'''
Basically a fading animation for a label
into the background,
because there is no option to set alpha value for
text colour in customtkinter


Produces a bit of a weird result if the no. of fade_steps
are a bit too high or the delay too low, work best with
white gradient 
'''
class FadeAnimation:
	# the anim_length is how many milliseconds you want the animation to last
	# best transition for 60 fade steps (found by debugging)
	def __init__(self, window : ctk.CTk, anim_length : int, text : str, text_clr : str, font : ctk.CTkFont, callback, steps=60):
		self.window = window
		self.window_bg = convert_clr_int(window.cget("fg_color"))
		self.original_clr = convert_clr_int(text_clr)
		self.label = ctk.CTkLabel(master = window,
			text = text,
			fg_color = "transparent",
			text_color = text_clr,
			font = font)

		self.fade_steps = steps
		self.fade_delay = anim_length // self.fade_steps
		self.count = 0
		self.callback = callback

	# triggers the fading effect 
	# WARNING : This class is only useful for fading, the reverse process cannot be done with this class
	def start(self) -> None:
		self.count += 1
		self.anim_triggered = True
		temp = [
		self.original_clr[i] + stepper(self.window_bg[i], self.original_clr[i], self.fade_steps) * self.count if self.original_clr[i] < self.window_bg[i] else self.original_clr[i] - stepper(self.window_bg[i], self.original_clr[i], self.fade_steps) * self.count for i in range(len(self.window_bg))
		] if self.count != self.fade_steps else self.window_bg
	
		self.label.configure(text_color = convert_clr_hex(temp))
		if self.count < self.fade_steps:
			self.window.after(self.fade_delay, self.start)
		else:
			self.callback()

	def make_visible(self):
		self.label.pack(expand = True, fill = 'both')

	def clear(self):
		self.label.pack_forget()


class Move:

	def __init__(self):
		self.delta = 1e-2
		self.x = 0
		self.y = 0
		self.delay = 0
		self.end = 0
		self.window = None

	# self callback function to change the x/y coordinate of the widget
	def animate(self, axis, put, func):
		callback = True
		if axis == "horizontal":
			if self.end > self.x:
				self.x += self.delta
			else:
				self.x -= self.delta
			if self.check_proximity(self.end, self.x, self.delta):
				callback = False
				self.x = self.end
		else:
			if self.end > self.y:
				self.y += self.delta
			else:
				self.y -= self.delta
			if self.check_proximity(self.y, self.end, self.delta):
				callback = False
				self.y = self.end

		put()
		if callback:
			self.window.after(self.delay, lambda: self.animate(axis, put, func))
		else:
			func()

	# multipurpose function to move any widget from one place to another in a given axis
	def move_widget(self, window : ctk.CTk, widget, x : float, y : float, end : float, axis : str, width : float, height : float, time : int, callback):
		if axis not in ["horizontal", "vertical"]: raise ValueError("axis can only be vertical or horizontal")
		self.window = window
		self.x = x
		self.y = y
		self.end = end
		self.calculate_delay(time, axis)
		self.animate(axis, lambda : widget.place(relx = self.x, rely = self.y, relwidth = width, relheight = height), callback)

	# checks whether x/y coordinate of current animated widget has reached within range of the end coordinate in the repective axis
	def check_proximity(self, point1, point2, grace):
		if point1 <= point2 <= point1 + grace or point1 >= point2 >= point1 - grace:
			return True
		return False

	# calculates delay for each frame prior to triggering the animation
	def calculate_delay(self, time, axis):
		steps = min(100, abs(self.end - (self.x if axis == "horizontal" else self.y)) / self.delta)
		self.delay = max(1, int(time / steps)) if steps != 0 else 0


