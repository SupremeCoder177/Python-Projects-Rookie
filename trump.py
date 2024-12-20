# Making a simple trumnp game in python (TUI Mode)

from random import shuffle, choice, randint
from time import sleep

class Game:

	def __init__(self):
		self.player_inven = list()
		self.comp_inven = list()
		self.top_card = list()
		self.playing = str()
		self.player_points = 0
		self.comp_points = 0
		self.make_deck()
		self.group_val = {
		'Spades' : 4,
		'Hearts' : 3,
		'Clubs' : 2,
		'Diamonds' : 1
		}
		self.card_val = {
			'Ace' : 1,
			'2' : 2,
			'3' : 3,
			'4' : 4,
			'5' : 5,
			'6' : 6,
			'7' : 7,
			'8' : 8,
			'9' : 9,
			'10' : 10,
			'King' : 11,
			'Queen' : 12,
			'Jack' : 13
		}
		self.start()

	def make_deck(self):
		cards = []
		card_groups = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
		for i in range(10):
			for group in card_groups:
				if i + 1 == 1:
					cards.append([group, 'Ace'])
				else:
					cards.append([group, str(i + 1)])
		for group in card_groups:
			cards.append([group, 'King'])
			cards.append([group, 'Queen'])
			cards.append([group, 'Jack'])

		shuffle(cards)

		self.distribute(cards)

	def distribute(self, cards):
		for i in range(52 // 2):
			self.player_inven.append(cards[i])
			cards.pop(i)
		for i in range(52 // 2):
			self.comp_inven.append(cards[i])

	def pick_start_player(self):
		if randint(0, 1):
			self.playing = 'you'
		else:
			self.playing = 'computer'

	def display_inven(self):
		count = 0
		for card in self.player_inven:
			print(f'{self.player_inven.index(card) + 1}. {card[0]} {card[1]}', end = '\t\t')
			if count != 3:
				count += 1
			else:
				print()
				count = 0
		print()

	def get_card_val(self, card):
		return self.group_val[str(card[0])] + self.card_val[card[1]]

	def compare_cards(self, card1, card2):
		return True if self.get_card_val(card2) > self.get_card_val(card1) else False

	def player_play_card(self):
		print("Here are the cards in your inventory, enter the card number to play it.", end = '\n\n')
		self.display_inven()
		if not self.top_card:
			print("Pick Any Card to play:")
		else:
			print(f"The top card is {self.top_card[0]} {self.top_card[1]}, pick card accordingly.")
		while True:
			try:
				player_card = int(input(">")) - 1
				if 0 <= player_card < len(self.player_inven): break
				else:
					print("Card Number Beyond Inventory Size !!")
			except Exception as e:
				print("Invalid Input !!")
		if not self.top_card:
			self.top_card = [player_card[0], player_card[1]]
		else:
			if self.compare_cards(self.top_card, player_card):
				self.player_points += 1
				self.playing = 'you'
			else:
				self.comp_points += 1
				self.playing = 'computer'
			self.top_card.clear()

		self.player_inven.remove(player_card)

	def lowest_possible(self, cards):
		vals = dict()
		for card in cards:
			vals.update({card : self.get_card_val(card)})
		return vals[min(list(vals.values()))]

	def comp_play_card(self):
		if not self.top_card:
			card = choice(self.comp_inven)
			self.top_card = card
		else:
			usable_cards = list()
			for card in self.comp_inven:
				if card[0] == self.top_card or self.group_val[card[0]] > self.group_val[self.top_card[0]]:
					usable_cards.append(card)
			if not usable_cards:
				card = choice(self.comp_inven)
			else:
				card = self.lowest_possible(usable_cards)
			if self.compare_cards(self.top_card, card):
				self.comp_points += 1
				self.playing = 'computer'
			else:
				self.player_points += 1
				self.playing = 'you'
			self.top_card.clear()
		
		self.comp_inven.remove(card)

	def start(self):
		print("Welcome...")
		print("Shuffling cards....")
		sleep(1)
		print("Distributing....")
		sleep(1)
		self.pick_start_player()
		while len(self.player_inven) != 0 or len(self.comp_inven) != 0: 
			if self.playing == 'you':
				self.player_play_card()
				self.comp_play_card()
			else:
				self.comp_play_card()
				self.player_play_card()
		print(f'You had {self.player_points} points.')
		print(f'The computer had {self.comp_points} points.')
		if self.player_points > self.comp_points:
			print("You won !!")
		else: print("Sorry you lost :( !!")


if __name__ == "__main__":
	Game()

