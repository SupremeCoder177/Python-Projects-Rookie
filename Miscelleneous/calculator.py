# Making a simple calculator in python

def add(num1, num2):
	return num1 + num2


def sub(num1, num2):
	return num1 - num2


def mul(num1, num2):
	return num1 * num2


def div(num1, num2):
	return num1 / num2


print("Welcome....")
while True:
	while True:
		try:
			num1 = int(input('Enter a number:'))
			num2 = int(input('Enter another number:'))
			break
		except Exception as e:
			print('Invalid Input !!')
	print('''
		1 = Add,
		2 = Subtract,
		3 = Multiply,
		4 = Divide,
		0 = Exit
		''')
	while True:
		try:
			choice = int(input("Enter your choice:"))
			if 0 <= choice <= 4:
				break
			else: print("Invalid Choice !!")
		except Exception as e:
			print("Invalid Input !!")

	if choice == 1:
		print(f"The numbers added are {add(num1, num2)}")
	elif choice == 2:
		print(f"The numbers subtracted are {sub(num1, num2)}")
	elif choice == 3:
		print(f"The numbers multiplied are {mul(num1, num2)}")
	elif choice == 4:
		print(f"The numbers divided are {div(num1, num2)}")
	else:
		print("Ok bye !!")
		break
