# a testing script for my levelLoader script


from levelLoader import PixelLevelLoader
import pygame as pg
import os
from sys import exit


def take_input(speed):
	global offset_x, offset_y
	keys = pg.key.get_pressed()
	if keys[pg.K_w] or keys[pg.K_UP]:
		offset_y += speed
	if keys[pg.K_s] or keys[pg.K_DOWN]:
		offset_y -= speed
	if keys[pg.K_a] or keys[pg.K_LEFT]:
		offset_x += speed
	if keys[pg.K_d] or keys[pg.K_RIGHT]:
		offset_x -= speed


pg.init()
screen = pg.display.set_mode((600, 400))
clock = pg.time.Clock()
pg.display.set_caption("Testing Level Loader")
tile_size = 50
loader = PixelLevelLoader("F:\\Pixel Levels\\Testing\\test13.json", True)
tiles = loader.get_positions()
images = loader.get_images()

offset_x = offset_y = 0

running = True
while running:
	for event in pg.event.get():
		if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
			running = False

	screen.fill((0, 0, 0))
	take_input(5)

	print(f'\roffset_x : {offset_y}, offset_y : {offset_y}', end = "")

	for tile_pos, image_path in tiles.items():
		image = images[image_path]
		x = tile_pos[0] * tile_size + offset_x
		y = tile_pos[1] * tile_size + offset_y
		screen.blit(image, (x, y))

	pg.display.flip()
	clock.tick(60)

print()
exit()