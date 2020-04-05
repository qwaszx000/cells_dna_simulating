from . import instruments as instruments

class Food:
	x: int = 0
	y: int = 0
	value: int = 3
	color: str = "#FF3030"
	color_outline: str = color
	__name__ = "Food"
	def __init__(self, x = -1, y = -1, value = 3, color = "#FF3030"):
		self.x = x
		self.y = y
		self.value = value

	def __str__(self):
		return self.__name__

	def __setattr__(self, name, value):
		#cast type to avoid errors. Like hp is str and other
		if not type(getattr(self, name)) == type(value):
			if type(getattr(self, name)) == int:
				value = int(value)
			if type(getattr(self, name)) == str:
				value = str(value)
			if type(getattr(self, name)) == float:
				value = float(value)

		super().__setattr__(name, value)