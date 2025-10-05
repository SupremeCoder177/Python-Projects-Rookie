1# this module handles the generation and management of
# the data, if you want to add more
# data types, then edit the variables here

from json import load
from typing import List
from random import randint, choice


DATA_TYPES = ["First Name", "Last Name", "Gender", "Email", "Number", "Date", "Address", "Boolean", "Geography", "Incremental (Primary Key)"]
DATA = None

try:
	if __name__ != "__main__":
		with open("utils/names_and_locations.json", "r") as f:
			DATA = load(f)
	else:
		with open("names_and_locations.json", "r") as f:
			DATA = load(f)
except FileNotFoundError as e:
	print("JSON file containing DATA could not be loaded ")


# returns the list of all possible locations stored in DATA
def get_locations() -> List[str]:
	return list(DATA.keys())


class DataGenerator:

	def __init__(self, console, master):
		self.console = console
		self.master = master
		self.data = []

		self.gen_func_mapping = {
		"First Name" :self.gen_name,
		"Last Name" : self.gen_name,
		"Number" : self.gen_number,
		"Date" : self.gen_date,
		"Boolean" : self.gen_bool,
		"Address" : self.gen_addr
		}

		# telling the user that the DATA is not loaded
		# and to try again 
		if not DATA:
			self.console.set_text("Error, json file not found !", 2000, "Make sure you didn't tamper with the files !")

	# this is the main function which calls the sub-funcitons to generate data
	def gen_data(self, column_data : List[any], num_rows : int) -> None:
		self.data = []
		heading_row = []
		for data in column_data:
			heading_row.append(data["name"])
	
		self.data.append(heading_row)
		num_columns = len(column_data)

		has_location, location_index = self.check_type_column(column_data, "Geography")
		has_first_name, name_index = self.check_type_column(column_data, "First Name")
		has_last_name, last_name_index = self.check_type_column(column_data, "Last Name")
		has_gender, gender_index = self.check_type_column(column_data, "Gender")
		has_email, email_index = self.check_type_column(column_data, "Email")

		# generating data row-wise
		for i in range(1, num_rows + 1):
			row = [None for j in range(num_columns)]

			# generating data related to names 
			# and locations and genders (basically interconnected data types)
			location = None
			if location_index >= 0 or has_first_name or has_last_name or has_email:
				location = self.gen_location()
				if has_location: row[location_index] = location

			gender = None
			if gender_index >= 0 or has_first_name or has_last_name or has_email:
				gender = choice(["Male", "Female"])
				if has_gender: row[gender_index] = gender

			first_name = None
			last_name = None
			if has_first_name or has_email:
				first_name = self.gen_name(location, gender = gender)
				if has_first_name: row[name_index] = first_name

			if has_last_name or has_email:
				last_name = self.gen_name(location, first = False, gender = gender)
				if has_last_name: row[last_name_index] = last_name

			if has_email:
				row[email_index] = self.gen_email(first_name, last_name)

			# generating independent data type values
			for j in range(num_columns):
				if j in (name_index, location_index, last_name_index, gender_index, email_index): continue

				d_type = column_data[j]["type"]

				if d_type == "Incremental (Primary Key)":
					row[j] = i
					continue

				lower = column_data[j]["lower"]
				upper = column_data[j]["upper"]
				row[j] = self.gen_func_mapping[d_type](lower, upper) 
			self.data.append(row)

	# generates a first/last name
	# a the given length = amount, and
	# belonging to the chosen location
	def gen_name(self, location : str, first = True, gender = "Male") -> str:
		country_data = DATA[location]
		name_data = None
		if first:
			if gender == "Male":
				name_data = country_data["firsts_male"]
			else:
				name_data = country_data["firsts_female"]
		else:
			name_data = country_data["lasts"]
		return choice(name_data)

	# returns a random location from the
	# available locations
	def gen_location(self) -> str:
		return choice(get_locations())

	# returns a number in the given range
	def gen_number(self, lower : int, upper : int) -> int:
		return randint(lower, upper)

	# returns a random date between the given two yeards
	def gen_date(self, lower : int, upper : int) -> str:
		year = randint(lower, upper)
		month = randint(1, 12)
		day = randint(1, 30)
		return f'{year}-{month}-{day}'

	# returns a true or a false
	def gen_bool(self, lower : int, upper : int) -> bool:
		return randint(0, 1) == 1

	# returns a random address
	def gen_addr(self, lower : int, upper : int) -> str:
		common_street_names = ["Avenue", "Baker", "Smith", "Local", "Garden", "Main Road", "Colony", "Highway"]
		street_number = randint(1, 200)
		return f'{choice(common_street_names)} {street_number} {choice(common_street_names)}'

	# returns a random email based on the given name
	def gen_email(self, first_name : str, last_name : str) -> str:
		max_len = len(first_name) + len(last_name)
		first_name_tokens = randint(1, len(first_name))
		last_name_tokens = max_len - first_name_tokens
		return f'{first_name[:first_name_tokens]}{randint(20, 100)}{last_name[:last_name_tokens]}@{choice(["gmail.com", "msn.net", "ggs.net", "asap.net", "fbnet.com"])}'

	# returns (True, col_index) if it finds the data type in the
	# column data, else (False, -1)
	def check_type_column(self, column_data : List[any], d_type : str) -> tuple[bool, int]:
		for index, data in enumerate(column_data):
			if data["type"] == d_type: return (True, index)
		return (False, -1)

	# self explanatory I think
	def get_data(self) -> List[any]:
		return self.data