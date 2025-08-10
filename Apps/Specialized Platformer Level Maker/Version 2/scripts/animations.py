# this module handles all the animations

from collections.abc import Callable
from typing import List
import customtkinter as ctk

# general purpose function to make a sliding animation of a frame
def move_frame(frame : ctk.CTkFrame, time : int, _from : List[float], to : List[float], callback : Callable):
	if not len(_from) == 2 or not len(to) == 2 or not isinstance(frame, ctk.CTkFrame):
		return

	# calculating the distance to travel
	distance_x = abs(_from[0] - to[0])
	distance_y = abs(_from[1] - to[1])

	# calculating the step to take
	step_size = max(distance_x, distance_y) / time

	# calculating the steps in each direction
	steps_x = distance_x / step_size
	steps_y = distance_y / step_size

	# calculating delay to recusive animate based on max number of steps
	delay = int(time / max(steps_x, steps_y))

	x, y = _from
	move_x = move_y = True

	def animate():
		nonlocal x, y, move_x, move_y
		if x - step_size < to[0] < x + step_size:
			move_x = False
		else:
			x += step_size if _from[0] < to[0] else -step_size
		if y - step_size < to[1] < x + step_size:
			move_y = False
		else:
			y += step_size if _from[1] < to[1] else -step_size

		if not (move_x or move_y):
			if callback: callback()
			frame.place(relx = to[0], rely = to[1])
		else:
			frame.place(relx = x, rely = y)
			frame.master.after(delay, animate)
	animate()

