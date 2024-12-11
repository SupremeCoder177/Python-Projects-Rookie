# making specific use case widgets

from settings import *
from math import sin, cos, tan


class Button(ctk.CTkButton):

	def __init__(self, parent, font, row, col, color, hvr_color, text_clr, command, text = ''):

		super().__init__(master = parent,
				text = text,
				font = font,
				fg_color = color,
				hover_color = hvr_color,
				text_color = text_clr,
				command = command,
				corner_radius = BUTTON_BORDER_RADIUS)

		self.grid(row = row, column = col, sticky = 'NSEW', padx = GAP, pady = GAP)


class Label(ctk.CTkLabel):

	def __init__(self, parent, font, row, col, color, text_clr, anchor, colspan, text_var):

		super().__init__(master = parent,
			font = font,
			fg_color = color,
			text_color = text_clr,
			textvariable = text_var)

		self.grid(column = col, row = row, sticky = anchor, columnspan = colspan)


class NormalLayout(ctk.CTkFrame):

	def __init__(self, parent):
		super().__init__(master = parent, fg_color = APP_BG)

		# making the frame layout
		self.rowconfigure(list(range(7)), weight = 1, uniform = 'a')
		self.columnconfigure(list(range(4)), weight = 1, uniform = 'a')

		# initializing global vars
		self.parent = parent
		self.num_list = list()
		self.equation = list()
		self.result_var = ctk.StringVar(value = '0')
		self.formula_var = ctk.StringVar(value = '')
		self.calculated = False

		self.add_widgets()

		self.pack(expand = True, fill = 'both')

	def add_widgets(self):
		self.make_labels()
		self.make_buttons()

	def make_labels(self):
		Label(parent = self, 
			font = self.parent.result_label_font,
			row = 1, 
			col = 0, 
			color = APP_BG, 
			text_clr = COLORS['label_text_color'], 
			anchor = 'E',
			colspan = 4,
			text_var = self.result_var)

		Label(parent = self, 
			font = self.parent.formula_label_font,
			row = 0, 
			col = 0, 
			color = APP_BG, 
			text_clr = COLORS['label_text_color'], 
			anchor = 'ES',
			colspan = 4,
			text_var = self.formula_var)

	def num_btn_func(self, text):
		if self.calculated:
			self.calculated = False
		if text == '.' and '.' in self.num_list:
			return
		else:
			if text == '.':
				self.num_list.append('0')
		if text == '0' and len(self.num_list) == 0:
			return

		self.num_list.append(text)
		self.result_var.set(''.join(self.num_list))
		self.formula_var.set(' '.join(self.equation))

	def ope_add_btn(self, ope):
		if ope != '=':
			if self.num_list:
				self.equation.append(''.join(self.num_list))
				self.num_list.clear()
				self.equation.append(ope)
				self.formula_var.set(' '.join(self.equation))
			if self.calculated:
				self.equation.append(self.result_var.get())
				self.equation.append(ope)
				self.formula_var.set(' '.join(self.equation))
				self.calculated = False
		else:
			self.calculate()

	def calculate(self):
		if self.num_list:
			self.equation.append(''.join(self.num_list))
			self.num_list.clear()
		if not self.equation:
			return
		if self.equation[len(self.equation) - 1] in OPE_BTNS:
			return
		
		result = eval(''.join(self.equation))
		if isinstance(result, float):
			result = round(result, 10)
		self.result_var.set(result)
		self.formula_var.set(' '.join(self.equation))
		self.equation.clear()
		self.calculated = True

		self.parent.history.insert(0, (self.formula_var.get(), str(result)))
		 
	def special_btn_func(self, func):
		if func == '%':
			self.percentagize()
		if func == '+/-':
			self.change_sign()
		if func == 'AC':
			self.clear()
		if func == 'exp':
			self.parent.change_layout()

	def clear(self):
		self.result_var.set('0')
		self.formula_var.set('')
		self.num_list.clear()
		self.equation.clear()
		self.calculated = False

	def percentagize(self):
		if not self.num_list:
			return
		num = float(''.join(self.num_list))
		num /= 100
		num = round(num, 10)
		self.num_list.clear()
		for ch in str(num):
			self.num_list.append(ch)
		self.result_var.set(''.join(self.num_list))

	def change_sign(self):
		if self.calculated:
			if self.result_var.get()[0] != '-':
				self.result_var.set('-' + self.result_var.get())
			else:
				self.result_var.set(self.result_var.get()[1:])

		if not self.num_list:
			return
		if self.num_list[0] != '-':
			self.num_list.insert(0, '-')
		else:
			del self.num_list[0]

		self.result_var.set(''.join(self.num_list))

	def make_buttons(self):
		for btn, para in BTNS.items():
			color = COLORS['nor_btn'] if btn not in OPE_BTNS else COLORS['operator_yellow']
			hvr_color = COLORS['nor_btn_hvr'] if btn not in OPE_BTNS else COLORS['operator_hvr']
			text_clr = COLORS['text_color']			
			if btn not in OPE_BTNS and btn not in SPECIAL_BTNS:
				command = lambda btn=btn: self.num_btn_func(btn)
			else:
				if btn in OPE_BTNS:
					command = lambda btn=btn: self.ope_add_btn(btn)
				else:
					command = lambda btn=btn: self.special_btn_func(btn)
			Button(parent = self,
				text = para['text'],
				font = self.parent.main_font,
				row = para['row'],
				col = para['col'],
				color = color,
				hvr_color = hvr_color,
				text_clr = text_clr,
				command = command)
			

class HistoryLabel(ctk.CTkLabel):

	def __init__(self, parent, background, font, text, text_clr, anchor):
		super().__init__(master = parent,
			fg_color = background,
			font = font,
			text = text,
			text_color = text_clr,
			anchor = anchor)


class ToggleFrame(ctk.CTkScrollableFrame):

	def __init__(self, parent):
		super().__init__(master = parent,
			fg_color = TOGGLE_FRAME_FG)

		self.y = 1
		self.at_start = True
		self.frames = []
		self.parent = parent

		self.place(relx = 0, rely = self.y,
			relwidth = 1,
			relheight = 1,
			anchor = 'nw')

	def animate_frame(self):
		if self.at_start:
			self.add_widgets()
			self.animate_upwards()
			self.parent.his_button.place_forget()
		else:
			self.animate_downwards()

	def animate_upwards(self):
		self.y -= 0.02
		self.place(relx = 0, rely = self.y,
			relwidth = 1,
			relheight = 1,
			anchor = 'nw')
		if self.y > 0:
			self.after(TIME_BET_FRAME, self.animate_upwards)
		else:
			self.at_start = False

	def animate_downwards(self):
		self.y += 0.02
		self.place(relx = 0, rely = self.y,
			relwidth = 1,
			relheight = 1,
			anchor = 'nw')
		if self.y < 1:
			self.after(TIME_BET_FRAME, self.animate_downwards)
		else:
			self.at_start = True
			self.parent.his_button.place(relx = 0.99, rely = 0.01, anchor = 'ne')
			self.forget_widgets()

	def forget_widgets(self):
		for frame in self.frames:
			frame.pack_forget()
		self.frames.clear()

	def add_widgets(self):
		self.frames.append(ctk.CTkFrame(self, fg_color = HSTRY_FRAME_FG))
		
		for i in range(len(self.parent.history)):
			self.frames.append(ctk.CTkFrame(self, fg_color = HSTRY_FRAME_FG))

		btn_frame = self.frames[0]

		ctk.CTkButton(btn_frame,
			text = '↓',
			fg_color = HSTRY_LABEL_FG,
			text_color = HSTRY_LABEL_TXT_CLR,
			hover_color = BUTTON_HVR_COLOR,
			command = self.animate_frame).pack(expand = True, side = 'left')

		btn_frame.pack(expand = True, fill = 'both', padx = PADDING, pady = PADDING)

		if len(self.frames) == 1:
			return

		for i in range(len(self.frames)):
			if i == 0: continue

			HistoryLabel(parent = self.frames[i], 
				background = HSTRY_LABEL_FG, 
				font = self.parent.formula_label_font, 
				text = self.parent.history[i - 1][0], 
				text_clr = HSTRY_LABEL_TXT_CLR,
				anchor = 'ne').pack(expand = True,
				fill = 'both',
				padx = PADDING,
				pady = PADDING)

			HistoryLabel(parent = self.frames[i], 
				background = HSTRY_LABEL_FG, 
				font = self.parent.result_label_font, 
				text = self.parent.history[i - 1][1], 
				text_clr = HSTRY_LABEL_TXT_CLR,
				anchor = 'e').pack(expand = True,
				fill = 'both',
				padx = PADDING,
				pady = PADDING)

			self.frames[i].pack(expand = True, fill = 'both', padx = PADDING,
				pady = PADDING)




class AdvancedLayout(ctk.CTkFrame):

	def __init__(self, parent):
		super().__init__(master = parent,
			fg_color = APP_BG)

		self.rowconfigure(list(range(7)), weight = 1, uniform = 'b')
		self.columnconfigure(list(range(6)), weight = 1, uniform = 'b') 
		self.parent = parent

		# vars
		self.result_var = ctk.StringVar(value = '0')
		self.formula_var = ctk.StringVar(value = '')
		self.num_list = list()
		self.equation = list()
		self.calculated = False
		self.trig_open = False
		self.open_brack = 0
		self.closed_brack = 0
		self.waiting_for_expo = False
		self.trig_ope = ''

		self.add_widgets()

		self.pack(expand = True, fill = 'both')

	def add_widgets(self):
		self.add_labels()
		self.add_buttons()

	def add_labels(self):
		Label(parent = self, 
			font = self.parent.formula_label_font,
			row = 0, 
			col = 0, 
			color = APP_BG, 
			text_clr = COLORS['label_text_color'], 
			anchor = 'SE',
			colspan = 7,
			text_var = self.formula_var)

		Label(parent = self, 
			font = self.parent.result_label_font,
			row = 1, 
			col = 0, 
			color = APP_BG, 
			text_clr = COLORS['label_text_color'], 
			anchor = 'E',
			colspan = 7,
			text_var = self.result_var)

	def num_btn_func(self, text):
		if self.waiting_for_expo and text == '.': return
		if self.calculated:
			self.calculated = False
		if text == '.' and '.' in self.num_list:
			return
		else:
			if text == '.':
				self.num_list.append('0')
		if text == '0' and len(self.num_list) == 0:
			return

		self.num_list.append(text)
		self.result_var.set(''.join(self.num_list))
		self.formula_var.set(' '.join(self.equation))

	def ope_add_btn(self, ope):
		if self.waiting_for_expo and ope != '=': return
		if self.trig_open and ope != '=': return
		if ope != '=':
			if self.num_list:
				self.equation.append(''.join(self.num_list))
				self.num_list.clear()
				self.equation.append(ope)
				self.formula_var.set(' '.join(self.equation))
			if self.calculated:
				self.equation.append(self.result_var.get())
				self.equation.append(ope)
				self.formula_var.set(' '.join(self.equation))
				self.calculated = False
		else:
			self.calculate()

	def calculate(self):
		if self.trig_open:
			if self.num_list:
				num = float(''.join(self.num_list[self.num_list.index('(') + 1:self.num_list.index(')')]))
			if self.calculated:
				num = float(self.result_var.get()[self.result_var.get().index('(') + 1:self.result_var.get().index(')')])
			if self.trig_ope == 'sin':
				result = sin(num)
			if self.trig_ope == 'cos':
				result = cos(num)
			if self.trig_ope == 'tan':
				result = tan(num)
			result = round(result, 15)
			self.result_var.set(str(result))
			self.calculated = True
			self.num_list.clear()
			self.trig_open = False
			self.equation.clear()
			self.parent.history.insert(0 ,(f'{self.trig_ope}({num})', str(result)))
			return
		if self.waiting_for_expo:
			if not self.num_list: return
			else:
				num = float(self.equation[self.equation.index('^') - 1])
				power = int(''.join(self.num_list))
				result = num ** power
				result = round(result, 15)
				self.result_var.set(str(result))
				self.calculated = True
				self.waiting_for_expo = False
				self.equation.clear()
				self.parent.history.insert(0, (f'{num} ^ {power}', str(result)))
				return

		if self.open_brack != self.closed_brack:
			return
		if self.num_list:
			self.equation.append(''.join(self.num_list))
			self.num_list.clear()
		if not self.equation:
			return
		if self.equation[len(self.equation) - 1] in OPE_BTNS:
			return
		
		result = eval(''.join(self.equation))
		if isinstance(result, float):
			result = round(result, 15)
		self.result_var.set(result)
		self.formula_var.set(' '.join(self.equation))
		self.equation.clear()
		self.calculated = True

		self.parent.history.insert(0, (self.formula_var.get(), str(result)))
		 
	def special_btn_func(self, func):
		if func == '%':
			self.percentagize()
		if func == '+/-':
			self.change_sign()
		if func == 'AC':
			self.clear()
		if func == 'exp':
			self.parent.change_layout()

	def clear(self):
		self.result_var.set('0')
		self.formula_var.set('')
		self.num_list.clear()
		self.equation.clear()
		self.calculated = False
		self.open_brack = 0
		self.closed_brack = 0
		self.trig_open = False
		self.waiting_for_expo = False

	def percentagize(self):
		if self.trig_open or self.open_brack > self.closed_brack: return
		if not self.num_list:
			return
		num = float(''.join(self.num_list))
		num /= 100
		num = round(num, 15)
		self.num_list.clear()
		for ch in str(num):
			self.num_list.append(ch)
		self.result_var.set(''.join(self.num_list))

	def change_sign(self):
		if self.trig_open or self.open_brack > self.closed_brack: return
		if self.calculated:
			if self.result_var.get()[0] != '-':
				self.result_var.set('-' + self.result_var.get())
			else:
				self.result_var.set(self.result_var.get()[1:])

		if not self.num_list:
			return
		if self.num_list[0] != '-':
			self.num_list.insert(0, '-')
		else:
			del self.num_list[0]

		self.result_var.set(''.join(self.num_list))

	def adv_special_btn_func(self, func):
		if func in TRIG_FUNCS:
			self.trig(func)
		if func == '(' or func == ')':
			self.brack(func)
		if func == 'sqr':
			self.raise_to(1/2)
		if func == 'cube_root':
			self.raise_to(1/3)
		if func == 'sq':
			self.raise_to(2)
		if func == 'raised_to':
			self.special_raise_to()
		if func == 'env':
			self.parent.switch_mode()

	def special_raise_to(self):
		if self.waiting_for_expo: return

		if not (self.num_list or self.calculated): return

		if self.num_list:
			self.equation.append(''.join(self.num_list))
			self.num_list.clear()
		if self.calculated:
			self.equation.append(self.result_var.get())
			self.calculated = False

		self.equation.append('^')
		self.formula_var.set(' '.join(self.equation))
		self.waiting_for_expo = True

	def raise_to(self, power):
		if self.calculated:
			result = float(self.result_var.get())
			result = result ** power
			result = round(result, 15)
			self.result_var.set(str(result))
		if self.num_list:
			num = float(''.join(self.num_list))
			num = num ** power
			num = round(num, 15)
			self.num_list.clear()
			for ch in str(num):
				self.num_list.append(ch)
			self.result_var.set(''.join(self.num_list))

	def brack(self, ope):
		if self.trig_open and ope == '(': return
		if ope == '(':
			self.num_list.append(ope)
			self.open_brack += 1
		else:
			if self.closed_brack < self.open_brack:
				self.num_list.append(ope)
				self.closed_brack += 1
		self.result_var.set(''.join(self.num_list))

	def trig(self, ope):
		if self.trig_open: return
		if not (self.num_list or self.calculated): return
		if self.num_list:
			self.num_list.insert(0, f'{ope}')
			self.num_list.insert(1, '(')
			self.num_list.insert(len(self.num_list), ')')
			self.result_var.set(''.join(self.num_list))
		if self.calculated:
			self.result_var.set(f'{ope}(' + self.result_var.get() + ')')
		self.trig_open = True
		self.trig_ope = ope

	def add_buttons(self):
		for btn, para in ADVANCED_BTNS.items():
			color = COLORS['nor_btn'] if btn not in OPE_BTNS else COLORS['operator_yellow']
			hvr_color = COLORS['nor_btn_hvr'] if btn not in OPE_BTNS else COLORS['operator_hvr']
			text_clr = COLORS['text_color']			
			if btn not in OPE_BTNS and btn not in SPECIAL_BTNS and btn not in ADVANCED_SPECIAL_BTNS:
				command = lambda btn=btn: self.num_btn_func(btn)
			else:
				if btn in OPE_BTNS:
					command = lambda btn=btn: self.ope_add_btn(btn)
				elif btn in ADVANCED_SPECIAL_BTNS:
					command = lambda btn=btn: self.adv_special_btn_func(btn)
				else:
					command = lambda btn=btn: self.special_btn_func(btn)
			Button(parent = self,
				text = para['text'],
				font = self.parent.main_font,
				row = para['row'],
				col = para['col'],
				color = color,
				hvr_color = hvr_color,
				text_clr = text_clr,
				command = command)