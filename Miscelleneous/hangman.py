# Making a simple hangman game in python

from random import choice, randint
from nltk.corpus import words

def get_random_word(min_length, max_length):
	words_list = words.words()

	filtered_words = [word.lower() for word in words_list if min_length <= len(word) <= max_length]

	return choice(filtered_words)


def hang(word, lvl):
	satisfied = False
	hanged_word = list()
	while not satisfied:
		for ch in word:
			if randint(0, lvl):
				hanged_word.append(ch)
			else:
				if hanged_word.count('_') < lvl:
					hanged_word.append('_')
				else:
					hanged_word.append(ch)
		if hanged_word.count('_') < lvl:
			hanged_word.clear()
			continue
		else: satisfied = True
	return ''.join(hanged_word )


print('Welcome...')
lvl = 1
max_tries = 5
running =  True
while running:
	tries = 0
	word = get_random_word(min(3 + lvl, 5), min((lvl * 2) + 2, 20))
	hanged_word = hang(word, lvl)
	
	print(f'Your word is {hanged_word}')
	print(f'You get {max_tries} tries.')
	while tries < max_tries:
		answer = str(input('>'))
		if answer == word:
			print("You got it !!")
			lvl += 1
			break
		else:
			print('Wrong !!')
			tries += 1
	if tries == max_tries: print(f"You have run out of tries.\nThe answer was {word}")

	print("Enter 0 to continue, 1 to exit.")
	while True:
		try:
			usr_choice = int(input('>'))
			if usr_choice not in [0, 1]:
				print("Invalid Input !!")
				continue
			if usr_choice == 0:
				break
			else: 
				print("Okay byee !!")
				running = False
				break
		except Exception as e:
			print("Invalid Input !!")

