# testing 

import customtkinter as ctk
from scripts import animations as anims

test = ctk.CTk()
test.geometry("500x500")
test.title("Testing")

test_frame = ctk.CTkFrame(test, fg_color = "red")
test_frame.place(relx = 0, rely = 0, relwidth = 0.2, relheight = 0.2)

def move_frame():
	anims.move_frame([0, 0], [0.5, 0], 1000, test_frame)

test.bind('<Escape>', lambda event: test.quit())
test.bind('<KeyPress-d>', lambda event: move_frame())
test.mainloop()