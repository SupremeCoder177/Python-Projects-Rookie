# Animating scripts for widgets
# with custom exceptions

import customtkinter as ctk
from typing import Optional


# custom Exceptions

# when the position given is not valid or not given
class PositionError(Exception):
	def __init__(self, *arg, **kwargs):
		pass

# when the input to an animation function is not the right type of widget
class InvalidWidget(Exception):
	def __init__(self, *arg, **kwargs):
		pass


# a multi animation function to move widgets
# assumens that the widget passed in is a customtkiner widget
def move(delta_x : float, delta_y : float, _from : list[float, float], to : list[float, float], widget, delay : int):
	epsilon = 1e-02 # 0.01
	x, y = _from
	x_reached = y_reached = False

	def animate(x, y, x_reached, y_reached):
		if not x - epsilon < to[0] < x + epsilon: x += delta_x
		else: x_reached = True
		if not y - epsilon < to[1] < y + epsilon: x += delta_y
		else: y_reached = True
		widget.place(relx = x, rely = y)
		if not (x_reached and y_reached):
			widget.master.after(delay, lambda: animate(x, y, x_reached, y_reached))
		else:
			widget.place(relx = to[0], rely = to[1])

	animate(x, y, x_reached, y_reached)
	


# move animation implementation for frames
def move_frame(_from : tuple[float, float], to : tuple[float, float], time : int, frame : ctk.CTkFrame, callback = None):
	if not isinstance(_from, tuple) or not isinstance(to, tuple):
		raise PositionError("_from/to should be a grid position of tuple type")
	if not isinstance(frame, ctk.CTkFrame):
		raise InvalidWidget("frame argument should be a CTkFrame")
	if not isinstance(time, int):
		raise ValueError("time field can only be integers")

	delta_x = abs(_from[0] - to[0]) / time
	delta_x = delta_x if to[0] > _from[0] else -delta_x
	delta_y = abs(_from[1] - to[1]) / time
	delta_y = delta_y if to[1] < _from[1] else -delta_y
	
	steps_x = abs(abs(_from[0] - to[0]) / delta_x) if delta_x != 0 else 0
	steps_y = abs(abs(_from[1] - to[1]) / delta_y) if delta_y != 0 else 0
	delay = int(time / max(steps_x, steps_y))

	move(delta_x, delta_y, _from, to, frame, delay)
	if callback: callback()
