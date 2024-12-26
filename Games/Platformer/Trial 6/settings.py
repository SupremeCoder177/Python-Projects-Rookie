import pygame as pg
from sys import exit
import json

SCREEN_SIZE = (800, 600)
TILE_SIZE = 50
FPS = 60

with open('map.json', 'r') as file:
	TILE_MAP = json.load(file)
if not file.closed: file.close()
