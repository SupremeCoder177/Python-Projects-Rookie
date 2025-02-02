# Customizations 

import customtkinter as ctk
from scripts.usables import AnimatedPanel
from scripts.settings import *

class CustomizationsPanels:

	def __init__(self, parent):
		self.selected_widget_customs = AnimatedPanel(parent, 0.3, 0.012, 0.1, 'horizontal', 0.3, 0.8, ANIM_PANEL_BG, '<', '>', DEFAULT_BTN_CLR, DEFAULT_BTN_HVR_CLR, 0.12, 1)

	def get_curr_customs(self):
		pass
		

