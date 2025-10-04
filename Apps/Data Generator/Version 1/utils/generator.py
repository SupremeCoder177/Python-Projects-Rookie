# this module handles the generation and management of
# the data, if you want to add more
# data types, then edit the variables here

from json import load
from typing import List


DATA_TYPES = ["First Name", "Last Name", "Gender", "Email", "Number", "Date", "Address", "Boolean", "Geography", "Incremental (Primary Key)"]
DATA = None

if __name__ != "__main__":
	with open("utils/names_and_addresses.json", "r") as f:
		DATA = load(f)
else:
	with open("names_and_addresses.json", "r") as f:
		DATA = load(f)


class DataGenerator:

	def __init__(self, console, master):
		self.console = console
		self.master = master
		self.data = []

		self.gen_func_mapping = {
		"First Name" : lambda location: self.gen_names(location),
		"Last Name" : lambda location: self.gen_names(location, first = False)
		}

	# this is the main function which calls the sub-funcitons to generate data
	def gen_data(self, column_data : List[any], num_rows : int) -> None:
		self.data = []
		heading_row = []
		for data in column_data:
			heading_row.append(data["name"])
	
		self.data.append(heading_row)
		num_columns = len(column_data)

		for i in range(1, num_rows + 1):
			temp = [None for i in range(num_columns)]
			self.data.append(temp)

	# generates a first/last name
	# a the given length = amount, and
	# belonging to the chosen location
	def gen_names(self, location : str, first = True) -> List[str]:
		pass

	# checks to see if there is a column with the data type of Geography
	# if there is one, then returns the index of that column
	def check_location_column(self, column_data : list[any]) -> tuple[bool, int]:
		for index, data in enumerate(column_data):
			if column_data["type"] == "Geography":
				return (True, index)
		return (False, -1)

	# returns a random location from the
	# available locations
	def gen_location(self):
		pass

	# self explanatory I think
	def get_data(self) -> List[any]:
		return self.data