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
		self.data = list()
		self.location = None

		self.gen_func_mapping = {
		"First Name" : lambda amount, location: self.gen_names(amount, location),
		"Last Name" : lambda amount, location: self.gen_names(amount, location, first = False)
		}

	# this is the main function which calls the sub-funcitons to generate data
	def gen_data(self, column_data : List[any], num_rows : int) -> dict:
		for column in column_data:
			temp = self.gen_func_mapping[column["name"]](num_rows)

	# generates a list of first/last names
	# a the given length = amount, and
	# belonging to the chosne location
	def gen_names(self, amount : int, location : str, first = True) -> List[str]:
		pass


