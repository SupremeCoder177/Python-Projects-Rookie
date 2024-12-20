# making a simple rock paper scissors game in python

from random import choice


print("Welcome...")
comp_choices = ['rock', 'paper', 'scissor']
player_choices = {
	1 : 'rock',
	2 : 'paper',
	3 : 'scissor'
}
running = True
while running:
	print('Enter 1 to play, and 0 to exit')
	while True:
		try:
			usr_choice = int(input(">"))
			if usr_choice in [0, 1]: break
			else:
				print("Invalid Input !!")
		except Exception as e:
			print("Invalid Input !!")
	if usr_choice == 0:
		print("Ok bye !!")
		break
	else:
		print("How many points do you want to compete for?")
		while True:
			try:
				points = int(input(">"))
				if 3 <= points: break
				else:
					print("You cannot compete for less than 3 points.")
			except Exception as e:
				print("Invalid Input !!")
		player_points = 0
		comp_points = 0
		while player_points != points and comp_points != points:
			print('''
1 = rock,
2 = paper,
3 = scissors,
0 = exit
			''')
			while True:
				try:
					plyr_choice = int(input(">"))
					if plyr_choice in [1, 2, 3, 0]: break
					else:
						print("Invalid Input !!")
				except Exception as e:
					print("Invalid Input !!")
			if plyr_choice == 0:
				running = False
				break
			comp_choice = choice(comp_choices)
			player_choice = player_choices[plyr_choice]
			print(f'You picked {player_choice} and the computer picked {comp_choice}')
			if comp_choice == player_choice:
				print("Draw.")
			else:
				if player_choice == 'rock':
					if comp_choice == 'scissor':
						player_points += 1
						print("Yay you got a point !!")
					else:
						comp_points += 1
						print("The computer got a point !!")
				if player_choice == 'paper':
					if comp_choice == 'rock':
						player_points += 1
						print("Yay you got a point !!")
					else:
						comp_points += 1
						print("The computer got a point !!")
				if player_choice == 'scissor':
					if comp_choice == 'paper':
						player_points += 1
						print("Yay you got a point !!")
					else:
						comp_points += 1
						print("The computer got a point !!")



