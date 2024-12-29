# Don't mind me just making another dumbshit program

# Anime's I wanna watch

wanna_watch_list = ['Cowboy Bebop',
					'Durarara x2 The Third Arc',
					'Witch Craft Works',
					'Nisekoi',
					'Neon Genesis Evangelion',
					'Dragon Ball GT',
					'Dragon Ball',
					'The Eminence In Shadow',
					'The Quintessential Quintuplets',
					'Tsundere Children',
					'Your Lie In April',
					'Date A Live',
					'Bleach',
					'Gin-Tama',
					'Full Metal Alchemist - Brotherhood',
					'Jujutsu Kaisen',
					'Demon Slayer',
					'Solo Leveling',
					'Naruto',
					'One Piece',
					'Sumomomo Momomo',
					'Daily Life Of High School Boys',
					'How To Raise A Boring Girlfriend',
					"An Archdemon's Dilemma: How to Love Your Elf Bride",
					'The Magical Girl and the Evil Lieutenant Used to Be Archenemies',
					'2.5 Dimensional Seduction',
					'The Devil Is a Part Timer',
					'Infinite Stratos',
					'Vinland Saga',
					'Berserk',
					'Vagabond',
					'Toradora!',
					'From Me to You',
					'Pseudo Harem',
					"JoJo's Bizzare Adventure",
					'Attack On Titan',
					'High School Dxd',
					'Dragon Ball Daima',
					'Azumanga Dioh',
					'Darling In The Franxx',
					'Hell Girl',
					'Violet Evergarden',
					'Run With the Wind',
					'12 Kingdoms',
					'Sliver Spoon',
					'Mononoke',
					'ACCA13'
				]

# Anime's I have watched 

watched_list = ['Dragon Ball Super',
				'One Punch Man',
				'Dragon Ball Z',
				'Scissor Seven', 
				'My Teen Romantic Comedy SNAFU Too',
				'My Hero Acadamia',
				'Terror In Resonance',
				'Mashle: Magic And Muscles',
				'The 100 girlfriend who really really really really really love you !!',
				'Golden Hour', 
				"My Stepmother's Daughter is my Ex", 
				'Twin Star Exocrists', 
				'Horimiya',
				'My Little Monster', 
				'Our Love Story: The Experienced You and The Inexperienced Me',
				'My Sempai is Annoying', 
				'Shikimori is Not Just A Cutie', 
				"Komi Can't Communicate",
				'Rent-A-Girlfriend', 
				'The Wrong Way to Use Healing Magic', 
				'The Misfit of the Demong King Acadmy',
				'The Daily Life of the Immortal King', 
				'And You Thought There Is Never A Girl Online',
				"Please don't toy with me Miss Nagatoro",
				'Tomo-Chan Is a Girl',
				'Love Lab',
				'Re: Creators',
				'Love Is War : Kauguya-Sama',
				'The World Is Still Beautiful',
				'My Dress Up Darling',
				'Suzuka',
				'Fuuka',
				'Undefeated Bahamut Chronicle',
				'Studio Apartment, Good Lighting, Angel Included',
				'Midori Days',
				'Clean Freak! Aoyama - kun',
				'The Demon Sword Master of Excalibur Acadamy',
				'The Pet Girl of Sakurasou',
				'Seitokai Yakuindomo',
				'Date a live',
				'Akashic Records of Bastard Magic Instructor',
				'Campione',
				'Rascal Does Not Dream of Bunny Girl Senpai',
				'The Angel Next Door Spoils Me Rotten',
				'AHO-GIRL',
				'TenPuru',
				'Science Fell In Love, So I Tried To Prove It',
				'We Never Learn : BOKUBEN',
				'Yunna and the Haunted Hot Sptrings',
				'Battle Game In 5 Seconds',
				'The Troubled Life of Miss Kotoura',
				'TONIKAWA: Over The Moon For You',
				'Viral Hit',
				'Parasyte -the maxim-',
				'Trapped in a Dating Sim: The World of Otome Games Is Tough for Mobs',
				'Seirei Gensouki: Spirit Chronicles',
				'Hokkaido Gals Are Super Adorable',
				'Classroom Of The Elite',
				"I'm Quitting Heroing",
				'Monthly Girls - Nozaki-Kun',
				'Lookism']

watched_list_movies = ['Josee, the Tiger and the Fish',
			    'The Tunnel to Summer, the Exit of Goodbyes',
			    'A Silent Voice',
			    'Momotaro The Undefeated',
			    'Hello World']


# A way to access all of these

import customtkinter as ctk
import requests
from tkinter import *
import json
from tkinter import ttk, messagebox
from webbrowser import open_new_tab


class App(ctk.CTk):

	def __init__(self, screen_size):
		super().__init__()

		x = (self.winfo_screenwidth() - screen_size[0]) // 2
		y = (self.winfo_screenheight() - screen_size[1]) // 2

		self.geometry(f'{screen_size[0]}x{screen_size[1]}+{x}+{y}')
		self.title("Anime Things")
		self.resizable(False, False)
		ctk.set_appearance_mode('dark')

		self.ANIM_LISTS = {
			0 : watched_list,
			1 : wanna_watch_list,
			2 : watched_list_movies,
			}

		with open('data/desc.json', 'r') as f:
			self.desc = json.load(f)

		self.add_widgets()

		self.bind("<Escape>", lambda event: self.quit())
		self.attributes('-topmost', True)
		self.mainloop()

	def add_widgets(self):

		text_font = ctk.CTkFont(family = 'Cascadia Mono', size = 15)

		self.columnconfigure(0, weight = 2, uniform = 'c')
		self.columnconfigure(1, weight = 1, uniform = 'c')
		self.rowconfigure(0, weight = 1, uniform = 'c')

		input_frame = ctk.CTkFrame(self, fg_color = '#1d1b1f',
			 corner_radius = 20)

		desc_frame = ctk.CTkFrame(self, fg_color = 'transparent')

		input_frame.rowconfigure((0, 1, 2, 3), weight = 1, uniform = 'a')
		input_frame.columnconfigure((0, 1), weight = 1, uniform = 'a')

		btn_frame = ctk.CTkFrame(input_frame, fg_color = 'transparent')
		self.current_var = ''

		for index in self.ANIM_LISTS:	
			ctk.CTkComboBox(input_frame,
				values = sorted(self.ANIM_LISTS[index]),
				corner_radius = 10,
				fg_color = '#eee',
				text_color = '#111',
				dropdown_fg_color = '#232224',
				dropdown_hover_color = '#121112',
				dropdown_text_color = '#eee',
				command = lambda event: self.load_desc(event)).grid(row = index, column = 1, padx = 10, pady = 10, sticky = 'EW')

		ctk.CTkLabel(input_frame,
			text = "Watched List",
			font = text_font).grid(row = 0, column = 0)

		ctk.CTkLabel(input_frame,
			text = "Wanna Watch List",
			font = text_font).grid(row = 1, column = 0)

		ctk.CTkLabel(input_frame,
			text = "Watched List (Movies)",
			font = text_font).grid(row = 2, column = 0)

		ctk.CTkButton(btn_frame,
			text = "Watch",
			font = text_font,
			fg_color = '#1dcf8a',
			hover_color = '#16a66e',
			text_color = '#111',
			corner_radius = 10,
			command = self.watch).pack(expand = True)

		ctk.CTkLabel(desc_frame,
			text = "Anime Description",
			font = text_font).pack(pady = 4)

		self.text = ctk.CTkTextbox(desc_frame,
			fg_color = '#eee',
			text_color = '#111',
			activate_scrollbars = False)

		self.text.pack(expand = True, fill = 'both', padx = 4, pady = 4)

		ctk.CTkButton(desc_frame,
			text = 'Save Changes',
			font = text_font,
			fg_color = '#1dcf8a',
			hover_color = '#16a66e',
			text_color = '#111',
			corner_radius = 5,
			command = self.save_changes).pack(expand = True)

		btn_frame.grid(row = 3, column = 0, columnspan = 2, sticky = 'NSEW')
		input_frame.grid(row = 0, column = 0, sticky = "NSEW", padx = 4)
		desc_frame.grid(row = 0, column = 1, sticky = 'NSEW', padx = 4)

	def load_desc(self, var):
		self.text.delete('1.0', 'end')
		self.current_var = var
		if var not in self.desc:
			self.text.insert('0.0', "Didn't Watch Yet so no description yet bruh.")
			return
		self.text.insert('0.0', self.desc[var])

	def save_changes(self):
		if self.current_var in self.desc:
			self.desc[self.current_var] = self.text.get('1.0', 'end')
		with open('data/desc.json', 'w') as file:
			json.dump(self.desc, file, indent = 4, sort_keys = True)
		with open('data/desc.json', 'r') as file:
			self.desc = json.load(file)
		if not file.closed: file.close()

	def watch(self):
		urls = ["https://animesugetv.to", "https://hianime.to", "https://aniwatchtv.to"]
		
		for url in urls:
			try:
				request = requests.get(url, timeout = 5)
				if request.status_code == 200:
					open_new_tab(url)
					return
				else: continue
			except Exception as e:
				if e == requests.ConnectionError:
					messagebox.showerror("Error", "No Internet Connection !!")
					return

		messagebox.showerror("Error", "No Working Site Found !!")


if __name__ == '__main__':
	App((700, 400))
