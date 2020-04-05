from . import instruments as instruments

class Gene:
	name: str = ""
	Alives = []
	color = ""
	__name__ = "Gene"
	def __init__(self, name = "Gene"):
		self.name = name

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

	def __str__(self):
		return self.name

	def addAlive(self, alive):
		if alive not in self.Alives:
			self.Alives.append(alive)
			#do some effect on alive. Like color or etc.

	def doAction(options={}):
		pass

#Makes organism avaible to fear of other danger organisms
#TODO organism run away from danger organisms
class AfraidGene(Gene):
	name = "fear gene"
	Alives = []
	color = "#FFFF00"
	__name__ = "AfraidGene"

	def __init__(self, name = "AfraidGene"):
		self.name = name

	def addAlive(self, alive):
		if alive not in self.Alives:
			self.Alives.append(alive)
			#do some effect on alive. Like color or etc.
			if(len(self.color) >= 6):
				alive.addColor(self.color)

	def doAction(self, options={}):
		field = options['field']

		actions_list = {
			"Move": 1,
			"Attack": 0 
		}

		move_map = []

		for x in range(len(field)):
			move_map.append([])
			for y in range(len(field[x])):
				move_map[x].append(0)

		for x in range(len(move_map)):
			for y in range(len(move_map[x])):
				if field[x][y] is not None and field[x][y].__name__ == "Alive":
					for dx in range(-1, 2):
						for dy in range(-1, 2):
							if x + dx <= 24 and y + dy <= 24:
								move_map[x+dx][y+dy] = -75

					move_map[x][y] = -100

		return move_map, actions_list

#runs for food
class FoodEatingGene(Gene):
	name = "food eating"
	Alives = []
	color = "#8B4513"
	__name__ = "FoodEatingGene"
	def __init__(self, name = "FoodEatingGene"):
		self.name = name

	def addAlive(self, alive):
		if alive not in self.Alives:
			self.Alives.append(alive)
			#do some effect on alive. Like color or etc.
			if(len(self.color) >= 6):
				alive.addColor(self.color)

	def doAction(self, options={}):
		field = options['field']

		actions_list = {
			"Move": 1,
			"Attack": 0 
		}

		move_map = []

		for x in range(len(field)):
			move_map.append([])
			for y in range(len(field[x])):
				move_map[x].append(0)

		for x in range(len(move_map)):
			for y in range(len(move_map[x])):
				if field[x][y] is not None and field[x][y].__name__ == "Food":
					for dx in range(-1, 2):
						for dy in range(-1, 2):
							if x + dx <= 24 and y + dy <= 24:
								move_map[x+dx][y+dy] = 75

					move_map[x][y] = 100


		return move_map, actions_list