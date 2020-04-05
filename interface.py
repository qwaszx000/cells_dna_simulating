from tkinter import *
from tkinter import ttk
from random import randint
#for modules, classes, objects and props
import inspect
import gc

from . import alive as Alive
from . import genes as Genes
from . import food as Food
from . import instruments as instruments

class Interface():
	root = None
	canvas = None

	Alives = []
	Genes = []
	Foods = []

	Field = []#2d array. See initField
	fieldSize: int = 25
	cellSize: int = 20

	module_combobox = None
	selected_module = None
	selected_module_name = ""

	class_combobox = None
	selected_class = None

	object_combobox = None
	selected_obj = None

	property_combobox = None
	selected_prop = None
	property_entry = None

	start_btn = None
	food_per_turn = 10

	next_alive_id = 0

	isGameStarted: int = 0

	__name__ = "Interface"

	def __init__(self):
		#creating root
		self.root = Tk()
		self.root.title("DNA life simulation")
		self.root.geometry("1000x600")
		#widgets
		self.canvas = Canvas(self.root, width=500, height=500)
		self.canvas.place(x=0, y=0)
		self.drawGameField()

		self.start_btn = ttk.Button(self.root, text="Start", command=self.startGame)
		self.start_btn.place(x=100, y=511)

		step_btn = ttk.Button(self.root, text="Step", command=self.gameStep)
		step_btn.place(x=300, y=511)

		#options
		frame_options = Frame(self.root, width=500, height=500)
		frame_options.place(x=500, y=0)

		self.module_combobox = ttk.Combobox(frame_options)
		self.module_combobox['values'] = ["Interface", "Alive", "Genes", "Food", "None"]
		self.module_combobox.current(0)
		self.module_combobox.place(x=10, y=10)
		self.module_combobox.bind("<<ComboboxSelected>>", self.moduleComboboxSelected)

		self.class_combobox = ttk.Combobox(frame_options)
		self.class_combobox['values'] = ["None"]
		self.class_combobox.place(x=210, y=10)
		self.class_combobox.bind("<<ComboboxSelected>>", self.classComboboxSelected)

		self.object_combobox = ttk.Combobox(frame_options)
		self.object_combobox['values'] = ["None"]
		self.object_combobox.place(x=10, y=100)
		self.object_combobox.bind("<<ComboboxSelected>>", self.objectComboboxSelected)

		self.property_combobox = ttk.Combobox(frame_options)
		self.property_combobox['values'] = ["None"]
		self.property_combobox.place(x=10, y=200)
		self.property_combobox.bind("<<ComboboxSelected>>", self.propertyComboboxSelected)

		self.property_entry = Entry(frame_options)
		self.property_entry.place(x=210, y=200)

		property_label = Label(frame_options, text="Property data")
		property_label.place(x=210, y=180)

		edit_btn = ttk.Button(frame_options, text="Save", command=self.editBtnClick)
		edit_btn.place(x=150, y=250)

		addAlive_btn = ttk.Button(frame_options, text="New alive", command=self.addAliveBtnClick)
		addAlive_btn.place(x=10, y=300)

		addFood_btn = ttk.Button(frame_options, text="New food", command=self.addFoodBtnClick)
		addFood_btn.place(x=150, y=300)


		self.initField()
		self.root.after(100, self.update)

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

	#===========================GUI events and button commands====================
	def setPropEntryText(self, text):
		self.property_entry.delete(0, END)
		self.property_entry.insert(0, text)

	def moduleComboboxSelected(self, event):
		if event.widget.get() == "None":
			self.class_combobox['values'] = ["None"]
			return

		self.selected_module = globals()[event.widget.get()]
		#interface is current module so self.selected_module already contains class
		if event.widget.get() == "Interface":
			self.class_combobox['values'] = ["Interface"]
		else:
			self.class_combobox['values'] = [name for name, i in inspect.getmembers(self.selected_module) if inspect.isclass(i)]

		if len(self.class_combobox['values']) == 0:
			self.class_combobox['values'] = [self.selected_module]

	def classComboboxSelected(self, event):
		if event.widget.get() == "None":
			self.object_combobox['values'] = ["None"]
			return

		if "__package__" in dir(self.selected_module):
			self.selected_module_name = self.selected_module.__name__.replace(self.selected_module.__package__ + ".", "").title()#dna_lifes.alive -> Alive
		else:
			self.selected_module_name = self.selected_module.__name__

		#interface is current module so self.selected_module already contains class
		if event.widget.get() == "Interface":
			self.selected_class = self.selected_module
		else:
			self.selected_class = getattr(globals()[self.selected_module_name], event.widget.get())

		self.object_combobox['values'] = self.getClassInstances(self.selected_class)

	def objectComboboxSelected(self, event):
		if "color_outline" in dir(self.selected_obj):
			self.selected_obj.color_outline = self.selected_obj.color

		if event.widget.get() == "None":
			self.property_combobox['values'] = []
			return

		self.property_combobox['values'] = list(vars(self.selected_class).keys())

		obj_name = event.widget.get()
		if "name" in dir(self.selected_class):
			self.selected_obj = self.findInstByVar(self.selected_class, "name", obj_name)
		else:
			self.selected_obj = self.findInstByVar(self.selected_class, "__name__", obj_name)

		if "color_outline" in dir(self.selected_obj):
			self.selected_obj.color_outline = "#FFFF00" #show selected object

	def propertyComboboxSelected(self, event):
		if event.widget.get() == "None":
			return

		self.selected_prop = event.widget.get()

		self.setPropEntryText(getattr(self.selected_obj, self.selected_prop))

	def editBtnClick(self):
		setattr(self.selected_obj, self.selected_prop, self.property_entry.get())
		self.initField()

	def addAliveBtnClick(self):
		self.Alives.append(Alive.Alive())

	def addFoodBtnClick(self):
		self.Foods.append(Food.Food())

	def startGame(self):
		self.isGameStarted =  0 if self.isGameStarted == 1 else 1
		self.start_btn['text'] = "Stop" if self.isGameStarted == 1 else "Start"

	def gameStep(self):
		self.spawnFood()
		for f in self.Foods:
			if f.value <= 0:
				self.Foods.remove(f)

		for a in self.Alives:
			self.drawGameField()
			if a.hp <= 0:
				self.Alives.remove(a)
			else:
				a.doAction(self.Field)

		

	#returns all objects, that are instances of class
	#c - class
	def getClassInstances(self, c):
		instances = []
		for obj in gc.get_objects():
			if isinstance(obj, c):
				instances.append(obj)
		return instances

	#finds instance by class and var
	def findInstByVar(self, c, var_name, var):
		inst_list = self.getClassInstances(c)
		for i in inst_list:
			if getattr(i, var_name) == var:
				return i

	#===========================work with game objects=========================
	#adds alive to alives list
	def addAlive(self, alive):
		self.Alives.append(alive)
		self.Field[alive.x][alive.y] = alive

	#adds gene to genes list
	def addGene(self, gene):
		if gene not in self.Genes:
			self.Genes.append(gene)

	def removeGene(self, gene):
		self.Genes.remove(gene)

	#adds gene to genes list
	def addFood(self, food):
		self.Foods.append(food)

	#=========================main game functions=====================
	#fills Field with None.
	def initField(self):
		self.Field = []
		for x in range(self.fieldSize):
			self.Field.append([])
			for y in range(self.fieldSize):
				self.Field[x].append(None)

	def clearField(self):
		#field is not generated yet
		if len(self.Field) == 0:
			return

		for x in range(self.fieldSize):
			for y in range(self.fieldSize):
				self.Field[x][y] = None

	#fills field with alive and food list units
	def fillField(self):
		self.clearField()
		for f in self.Foods:
			if f.x in range(self.fieldSize) and f.y in range(self.fieldSize):
				self.Field[f.x][f.y] = f

				for a in self.Alives:
					if a.x in range(self.fieldSize) and a.y in range(self.fieldSize):
						self.Field[a.x][a.y] = a

						#alive eats food
						if a.x == f.x and a.y == f.y:
							if f in self.Foods:
								self.Foods.remove(f)
							self.Field[f.x][f.y] = a
							a.hp += 25

							if a.canBornAlive():
								a_children = a.createChildren(str(self.next_alive_id), self.fieldSize, self.Genes)
								self.Alives.append(a_children)
								self.next_alive_id += 1


		
	#draws grid in canvas. 
	def drawGrid(self, cellSize=20):
		#canvas sizes
		width = int(self.canvas['width'])
		height = int(self.canvas['height'])
		self.fieldSize = int(width / cellSize)
		#draw borders
		self.canvas.create_line(1, 0, 1, height)
		self.canvas.create_line(0, 1, width, 1)
		self.canvas.create_line(width-1, 0, width-1, height)
		self.canvas.create_line(0, height, width, height)

		#vertical lines
		for i in range(0, width, cellSize):
			self.canvas.create_line(i, 0, i, height)
		#horizontal lines
		for i in range(0, height, cellSize):
			self.canvas.create_line(0, i, width, i)

	#draws field objects 
	def drawObjects(self):
		for fx in self.Field:
			for obj in fx:
				if obj is None:
					continue
				#+1 and -1 need to show borders
				x = obj.x * self.cellSize
				y = obj.y * self.cellSize
				self.canvas.create_rectangle(x + 1, y + 1, x + self.cellSize - 1, y + self.cellSize - 1, outline=obj.color_outline, fill=obj.color)

	#draws all game field.
	#grid, borders, food, alive, dead, etc...
	def drawGameField(self):
		self.canvas.delete("all")#clear
		self.drawGrid(self.cellSize)
		self.fillField()
		self.drawObjects()

	def spawnFood(self):
		for i in self.Foods:
			i.value -= 1

		for i in range(self.food_per_turn):
			f = Food.Food(randint(0, self.fieldSize-1), randint(0, self.fieldSize-1))

			#food cant spawn in cell, where already food
			for sf in self.Foods:
				if sf.x == f.x and sf.y == f.y:
					return

			self.Foods.append(f)

	#main draw and logic function
	def update(self):
		self.drawGameField()
		if self.isGameStarted == 1:
			self.gameStep()

		self.root.after(100, self.update)

	#starts window main loop
	def start(self):
		self.root.mainloop()
