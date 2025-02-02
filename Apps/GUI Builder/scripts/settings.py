import customtkinter as ctk
import tkinter as tk
import ttkbootstrap as ttk

RECOG_WIDGETS = {
	'BUTTON': {'tkinter' : tk.Button,
			   'customtkinter' : ctk.CTkButton,
			   'ttkbootstrap' : ttk.Button},
	'LABEL' : {'tkinter' : tk.Label,
			   'customtkinter' : ctk.CTkLabel,
			   'ttkbootstrap' : ttk.Label}
}

WIDGET_CUSTOMS = {
	tk.Button : ('text', 'bg', 'fg', 'compound', 'textvariable', 'font', 'command', 'master'),
	tk.Label : ('text', 'bg', 'fg', 'compound', 'textvariable', 'font', 'master'),
	ctk.CTkButton : ('fg_color', 'text_color', 'hover_color', 'font', 'command', 'master'),
	ctk.CTkLabel : ('fg_color', 'text_color', 'font', 'width', 'height', 'master')
}

temp = ctk.CTk()
SLIDER_FRAME_FONT = ctk.CTkFont(family = 'Cascadio Mono', size = 15)
DEFAULT_FONT = ctk.CTkFont(family = 'Cascadio Mono', size = 20)
del temp

DEFAULT_BTN_CLR = '#4c20bd'
DEFAULT_BTN_HVR_CLR = '#33128a'
SLIDER_FRAME_CLR = '#1a1c1a'
SLIDER_FRAME_BTN_CLR = '#23a123'
SLIDER_FRAME_BTN_HVR_CLR = '#1b801b'
SLIDER_FRAME_PROGRESS_CLR = '#23a123'
ANIM_PANEL_BG = '#171515'
WIDGET_BTN_CLR = '#db16ad'
WIDGET_BTN_HVR_CLR = '#a61283'