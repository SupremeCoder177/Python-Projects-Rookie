# Making a simple number guessing game in python

from random import randint


answer = randint(1, 10)
no_of_tries = 0
while True:
	try:
		guess = int(input("Enter a number(1-10) :"))
		if guess == answer:
			print("You have guessed the number correctly !!")
			print(f"Tries : {no_of_tries}")
			break
		else:
			print("Incorrect guess !!")
			no_of_tries += 1
	except Exception as e:
		print("Invalid Input !!")


