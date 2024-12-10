# setting for calculator app

from darkdetect import isDark
import customtkinter as ctk

is_dark = isDark()

icon = 'Images\\dark.ico' if is_dark else 'Images\\light.ico'
APP_BG = ["#eeeeee", '#000000']
BUTTON_HVR_COLOR = ['#bbbbbb', '#333333']
TITLE_COLOR = 0x00000000 if is_dark else 0x00EEEEEE
APP_SIZE = (450, 650)
APP_MAX_SIZE = (APP_SIZE[0] + 250, APP_SIZE[1])
MARGIN = APP_MAX_SIZE[0] * 0.25
MAIN_FONT_SIZE = 40
RESULT_LABEL_FONT_SIZE = 70
FORMULA_LABEL_FONT_SIZE = 40
GAP = 1
COLORS = {
	'nor_btn' : ('#121211', '#c7c5bf'),
	'operator_yellow' : ('#f26d0f', '#f26d0f'),
	'nor_btn_hvr' : ('#0f0f0f', '#a1a197'),
	'operator_hvr' : ('#cf5c0a', '#cf5c0a'),
	'text_color' : ('#eeeeee', '#000000'),
	'label_text_color' : ('#000000', "#eeeeee")
}


BTNS = {
	'0' : {'text' : '0', 'row' : 6, 'col' : 0, 'colspan' : 2},
	'.' : {'text' : '.', 'row' : 6, 'col' : 2},
	'1' : {'text' : '1', 'row' : 5, 'col' : 0},
	'2' : {'text' : '2', 'row' : 5, 'col' : 1},
	'3' : {'text' : '3', 'row' : 5, 'col' : 2},
	'4' : {'text' : '4', 'row' : 4, 'col' : 0},
	'5' : {'text' : '5', 'row' : 4, 'col' : 1},
	'6' : {'text' : '6', 'row' : 4, 'col' : 2},
	'7' : {'text' : '7', 'row' : 3, 'col' : 0},
	'8' : {'text' : '8', 'row' : 3, 'col' : 1},
	'9' : {'text' : '9', 'row' : 3, 'col' : 2},
	'AC' : {'text' : 'AC', 'row' : 2, 'col' : 0},	
	'%' : {'text' : '%', 'row' : 2, 'col' : 1},	
	'+/-' : {'text' : '+/-', 'row' : 2, 'col' : 2},	
	'+' : {'text' : '+', 'row' : 2, 'col' : 3},	
	'-' : {'text' : '-', 'row' : 3, 'col' : 3},	
	'*' : {'text' : '*', 'row' : 4, 'col' : 3},	
	'/' : {'text' : '÷', 'row' : 5, 'col' : 3},	
	'=' : {'text' : '=', 'row' : 6, 'col' : 3},	
}

OPE_BTNS = {'+', '-', '/', '*', '='}
SPECIAL_BTNS = {'AC', '%', '+/-'}
