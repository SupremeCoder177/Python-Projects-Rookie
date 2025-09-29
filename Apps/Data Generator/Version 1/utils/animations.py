# this module handles all the animations

import customtkinter as ctk


class Animations:

	# slides a frame in the horiztonal axis in the given time and calls the callback function at the end of animation
	def slide_frame_horizontal(self, frame : ctk.CTkFrame, start_x : int, end_x : int, y : int, time : int, callback = lambda: None) -> None:
		dis = abs(end_x - start_x)
		delta = dis / time if end_x > start_x else -dis / time
		delay = int(time / (dis / abs(delta)))
		master = frame.master
		x = start_x

		# checks if an int is in a close enough range of another int
		def check_proximity(x1, x2) -> bool:
			if abs(x2 - x1) <= 0.01: return True
			return False

		# this is the recusive function that actually animated the frame
		def animate() -> None:
			nonlocal end_x, x, y
			x += delta
			frame.place(relx = x, rely = y)
			if check_proximity(x, end_x):
				frame.place(relx = end_x, rely = y)
				callback()
			else:
				master.after(delay, animate)
		animate()

	# this function handles the animation of a text in the app console, and calls the callback
	def animate_text(self, console, start_text : str, end_text : str, adder_character : str, time : int, callback = lambda: None) -> None:
		text = start_text
		delta = int(time / (len(end_text) - len(start_text)) / len(adder_character))
		master = console.master

		# this is the recusive function that animated the text
		def animate():
			nonlocal text, console, delta, end_text
			console.set_text(text, delta, text)
			text += adder_character
			if text == end_text or len(text) >= len(end_text):
				callback()
			else:
				master.after(delta, animate)
		animate()