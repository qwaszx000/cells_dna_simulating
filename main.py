from . import interface as GUI
from . import alive as Alive
from . import genes as Genes
from . import food as Food

#Simulation game
#Player sets genes for alive
#Player can create more then 1 alive by selecting object_combobox "Create new"
#Player click on cells to set it to chosen alive
#Player clicks on start_btn to start game.
#Python 3.6-tk required
def main():
	interface = GUI.Interface()

	f = Food.Food(1, 1)
	a = Alive.Alive("test1", 3, 3)
	g = Genes.FoodEatingGene()
	ga = Genes.AfraidGene()

	a.addGene(g)
	a.addGene(ga)
	
	interface.addGene(g)
	interface.addFood(f)
	interface.addAlive(a)

	interface.start()

if __name__ == '__main__':
	main()