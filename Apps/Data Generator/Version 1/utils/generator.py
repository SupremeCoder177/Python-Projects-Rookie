# this module handles the generation and management of
# the data, if you want to add more
# data types, then edit the variables here

from json import load


DATA_TYPES = ["First Name", "Last Name", "Gender", "Email", "Number", "Date", "Address", "Boolean", "Geography", "Incremental (Primary Key)"]
DATA = None

if __name__ != "__main__":
	with open("utils/names_and_addresses.json", "r") as f:
		DATA = load(f)
else:
	with open("names_and_addresses.json", "r") as f:
		DATA = load(f)