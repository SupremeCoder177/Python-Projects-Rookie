# the app settings are contained in this file
# and is directly linked to the json file in the same folder
# change settings in here to work with the same settings in the json file
# or redfine the base settings inside the settings.json file

from json import load
from os import getcwd
from sys import exit
import pygame as pg

SETTINGS = None

try:
	with open("settings.json", "r") as f:
		SETTINGS = load(f)
except FileNotFoundError as e:
	print("Settings not found in current working directory")
	print("Please make sure there is a 'settings.json' file in the current working folder")
	print(f"Current working folder : {getcwd()}")
	exit()


pg.font.init()
FONTS = {f : pg.font.Font(fp) for f, fp in SETTINGS["fonts"].items()}

COLOR_PALLATE = SETTINGS["color_pallate"]

# the loading screen settings are defined here
loading_screen_settings = {
	
}