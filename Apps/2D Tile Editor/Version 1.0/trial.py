import customtkinter as ctk
from PIL import ImageTk, Image
from random import randint

# RESULT : Tkinter Canvas cannot handle more than 1000 images at once, gonna have to use Pygame approach after all


SCREEN_SIZE = (500, 500)
FPS = 60

def animate():
	global img_index, anim_speed, images, canvas, window
	canvas.delete("all")
	img_index += anim_speed
	img_index %= len(images)


def load_image(path):
	return ImageTk.PhotoImage(Image.open(path).resize((50, 25)))


def draw_images(num):
	global canvas, img_index, images
	arr = []
	for i in range(num):
		arr.append(canvas.create_image(positions[i][0], positions[i][1], image = images[int(img_index)]))


def update():
	global window
	animate()
	draw_images(1000)
	window.after(1000 // FPS, update)

window = ctk.CTk()

canvas = ctk.CTkCanvas(window, width = SCREEN_SIZE[0], height = SCREEN_SIZE[1], bg="white")
canvas.pack()

positions = []

for i in range(1000):
	positions.append([randint(0, SCREEN_SIZE[0]), randint(0, SCREEN_SIZE[1])])

images = [load_image("Cloud1/cloud1.png"), load_image("Cloud1/cloud2.png"), load_image("Cloud1/cloud3.png")]
img_index = 0
anim_speed = 0.1
img_id = None

window.bind("<Escape>", lambda event: window.quit())
window.after(1000 // FPS, update)
window.mainloop()