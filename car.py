# Making a simple car program in python

class Car:

	def __init__(self, brand, name):
		self.brand = brand
		self.name = name
		self.state = 'Stopped'

	def start(self):
		if self.state == "Stopped":
			print("The car is started !!")
			self.state = "Started"
		else:
			print("The car is already started !!")

	def stop(self):
		if self.state == "Started":
			print("The car is stopped")
			self.state = 'Stopped' 
		else:
			print("The car is already stopped !!")


if __name__ == "__main__":
	car1 = Car('Tesla', 'Cybertruck')
	car1.start()
	car1.stop()
