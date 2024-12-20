# Making a simple password generator

from random import choice

chars = [ch for ch in 'abcdefghijklmnopqrstuvwxyz1234567890!~@#$%^&*()_+-=`']
print("Welcome....")
print("Enter the length of the required password you want to generate")
while True:
	try:
		length = int(input(">"))
		if not 10 <= length:
			print("Password length must be more than 10 characters !!")
		else: break
	except Exception as e:
		print("Invalid Input !!")

print(''.join([choice(chars) for i in range(length)]))

