from random import choice, randint
from . import instruments as instruments

class Alive:
	name: str = ""
	hp: int = 100
	speed: int = 1
	attack = 0

	color: str = "#005500" 
	color_outline: str = color

	Genes = []

	x: int = 0
	y: int = 0
	__name__ = "Alive"
	def __init__(self, name = "New Alive", x = -1, y = -1, hp = 100):
		self.name = name
		self.x = x
		self.y = y
		self.hp = hp
		self.Genes = []

	def __str__(self):
		return self.name

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

	#work with genes list
	def addGene(self, gene):
		if gene not in self.Genes:
			self.Genes.append(gene)

			#give gene access to alive
			gene.addAlive(self)

	def removeGene(self, gene):
		self.Genes.remove(gene)

	#if alive can born new child
	def canBornAlive(self):
		return self.hp >= 200

	def setColor(self, color):
		self.color = color
		self.color_outline = color

	def addColor(self, color):
		#rgb (self.color + color)/2
		self.setColor(instruments.IntToRGB( (instruments.RGBToInt(self.color)+instruments.RGBToInt(color)) // 2 ))


	def createChildren(self, child_id, fieldSize, all_genes, mutation_chance = 5):
		self.hp -= 100

		#spawn child in random cell
		child_x = self.x+randint(-1, 1)
		child_y = self.x+randint(-1, 1)
		while child_x not in range(fieldSize) and child_y not in range(fieldSize):
			child_x = self.x+randint(-1, 1)
			child_y = self.x+randint(-1, 1)

		a_children = Alive(self.name.split(" ")[0] + " " + child_id, child_x, child_y)

		for g in self.Genes:
			#mutation_chance to lose parent gene
			if mutation_chance > 0:
				roll = randint(0, 100//mutation_chance - 1)
			else:
				roll = 1

			if not roll == 0:
				a_children.addGene(g)

		for g in all_genes:
			#mutation_chance to get any gene
			if mutation_chance > 0:
				roll = randint(0, 100//mutation_chance - 1)
			else:
				roll = 1

			if roll == 0:
				a_children.addGene(g)

		return a_children


	#field shows to alive, what it see
	def doAction(self, field):
		self.hp -= 5 #starvation
		#shows alives want to move to specific positions
		#fill map with 0. 
		#So alive want move to all positions equally
		move_map = []
		prefered_action = None
		prefered_move = (1, 0)

		for x in range(len(field)):
			move_map.append([])
			for y in range(len(field[x])):
				move_map[x].append(0)

		actions_list = {
			#"Eat": 0,   #eat random nearest food or by prefered_move
			"Move": 1,  #move by prefered_move
			"Attack": 0 #attack random nearest alive or by prefered_move
		}

		#genes sets weights to actions and map positions
		for g in self.Genes:
			gene_moves, gene_actions = g.doAction(dict(field=field)) 

			for x in range(len(gene_moves)):
				for y in range(len(gene_moves[x])):
					move_map[x][y] += gene_moves[x][y]

			for key, value in gene_actions.items():
				actions_list[key] += gene_actions[key]

		#where we can step in this turn
		best_move = -9999
		posible_moves = []
		for dx in range(-1, 2):
			for dy in range(-1, 2):
				if self.x + dx in range(len(field)) and self.y + dy in range(len(field[0])):
					if type(field[self.x+dx][self.y+dy]) is not Alive:
						#better move
						if move_map[self.x+dx][self.y+dy] > best_move:
							posible_moves = []
							best_move = move_map[self.x+dx][self.y+dy]
							posible_moves.append( (dx, dy) )
							prefered_move = (dx, dy)
						#similar move
						if move_map[self.x+dx][self.y+dy] == best_move:
							posible_moves.append( (dx, dy) )

		if not posible_moves == []:
			prefered_move = choice(posible_moves)

		prefered_action = max(actions_list, key=lambda key: actions_list[key])
		if prefered_action == "Move":
			self.x += prefered_move[0]
			self.y += prefered_move[1]
		elif prefered_action == "Attack":
			pass
		else:
			pass

		