# Making A simple bank program in python

accounts = {
	'Peter Banks' : {'password' : 892323,
					 'social_security_number' : 345654,
					 'balance' : 45000}
}

def change_balance(choice, name):
	while True:
		if choice == 2:
			print("Enter amount to deposit")
		else: print("Enter amount to Withdraw")
		try:
			amount = int(input(">"))
			if amount <= 0:
				print("Amount cannot be negative or zero.")
				continue

			if choice == 2:
				print("Amount has been deposited succesfully.")
				accounts[name]['balance'] = accounts[name]['balance'] + amount
				break
			else:
				if amount > accounts[name]['balance']:
					print("Cannot Withdraw more than balance !!")
				else:
					print("Amount has been withdrawed.")
					accounts[name]['balance'] = accounts[name]['balance'] - amount
					break
		except Exception as e:
			print('Invalid Input !!')

	return None


def account_login():	
	name = input("Enter your name:")
	if accounts.get(name, -1) == -1: 
		print("No account under the name, you can make one though.")
		return False, None
	else:
		try:
			password = int(input("Enter password (1 try only):"))
			social_num = int(input("Enter social security number (1 try only):"))
			if password == accounts[name]['password'] and social_num == accounts[name]['social_security_number']:
				return True, name
			else:
				print("Invalid Credentials !!")
				return False, None
		except Exception as e:
			print("Invalid Input !!")


def make_account():
	print("Enter your name please")
	name = input(">")
	while True:
		try:
			password = int(input("Please enter a 6-digit password:"))
			if len(str(password)) != 6:
				print("Invalid Password Length !!")
			else:
				social_num = int(input("Enter your social security number:"))
				break
		except Exception as e:
			print("Invalid Input !!")
	accounts.update({name : {'password' : password, 'social_security_number' : social_num, 'balance' : 0}})
	print("Account Initialized succesfully.")
	return None



print("Welcome...")
while True:
	print('''
0 = Exit,
1 = Login Into Account
2 = Make New Account
		''')
	while True:
		try:
			choice = int(input(">"))
			if choice not in [0, 1, 2]:
				print("Invalid Choice !!")
			else: break
		except Exception as e:
			print("Invalid Input !!")
	if choice == 0: break
	elif choice == 1:
		access, name = account_login()
		if access:
			while True:
				print('''
1 = See Balance,
2 = Deposit,
3 = Withdraw,
4 = Exit
				''')
				while True:
					try:
						usr_choice = int(input(">"))
						if usr_choice not in [1, 2, 3, 4]: print("Invalid Input !!")
						else: break
					except Exception as e:
						print("Invalid Input !!")
				if usr_choice == 1:
					print(f"Balance : ${accounts[name]['balance']}")
				elif usr_choice in [2, 3]:
					change_balance(usr_choice, name)
				else: break
	else:
		make_account()

