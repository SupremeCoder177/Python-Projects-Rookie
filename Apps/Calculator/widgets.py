# making specific use case widgets

from settings import *


class Button(ctk.CTkButton):

	def __init__(self, parent, font, row, col, color, hvr_color, text_clr, colspan, command, text = ''):

		super().__init__(master = parent,
				text = text,
				font = font,
				fg_color = color,
				hover_color = hvr_color,
				text_color = text_clr,
				command = command)

		self.grid(row = row, column = col, sticky = 'NSEW', padx = GAP, pady = GAP, columnspan = colspan)


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
		 
	def special_btn_func(self, func):
		if func == '%':
			self.percentagize()
		if func == '+/-':
			self.change_sign()
		if func == 'AC':
			self.clear()

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
		if not self.num_list:
			return
		if self.num_list[0] != '-':
			self.num_list.insert('-', 0)
		else:
			del self.num_list[0]

	def make_buttons(self):
		for btn, para in BTNS.items():
			color = COLORS['nor_btn'] if btn not in OPE_BTNS else COLORS['operator_yellow']
			hvr_color = COLORS['nor_btn_hvr'] if btn not in OPE_BTNS else COLORS['operator_hvr']
			text_clr = COLORS['text_color']			
			colspan = 1 if not para.get('colspan', None) else 2
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
				colspan = colspan,
				color = color,
				hvr_color = hvr_color,
				text_clr = text_clr,
				command = command)
			
