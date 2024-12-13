# making a photo editor in python

import customtkinter as ctk
from PIL import Image, ImageTk, ImageEnhance, ImageFilter, ImageOps
from darkdetect import isDark

is_dark = isDark()

APP_BG = ('#eeeeee', '#111111')
PANEL_BG = ('#dddddd', '#242424')
PANEL_CORNER_RADIUS = 10
APP_SIZE = (1400, 800)
BTN_COLOR = '#0d0db5'
BTN_HVR_CLR = '#0b0ba1'
ICON = 'Images\\icon.ico'
PADDING = 10
FONT = 'Cascadia Mono'
LABEL_FONT_SIZE = 14
TEXT_COLOR = ('#000000', '#ffffff')
PANEL_WIDGET_BG = ('#bbbbbb', '#343434')
SLIDER_BG = ('#111111', '#eeeeee')
CLOSE_RED = '#ed0919'
CLOSE_FG = ('#ddddd', '#343434')
SAVE_BTN_COLOR = '#a015bf'
SAVE_BTN_HVR_CLR = '#820e9c'
OPTION_FRAME_BG = '#343434'
OPTION_FRAME_BTN_HVR_CLR = ('#2b2a29','#999896')