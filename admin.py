import sys, pickle

sys.path.append("roguey/classes")

from items import Treasure
from constants import *


class Admin(object):
	def __init__(self):
		f = open("roguey/resources/items.pk")
		try:
			self.treasures = pickle.load(f)
		except:
			print "No treasures!"
			self.treasures = []
		f.close()
		self.main()

	def new_treasure(self):
		for treasure in TREASURE_TYPES:
			print "%s. %s" % (TREASURE_TYPES.index(treasure)+1, treasure)
		choice = raw_input("Pick a type [1-9]: ")
		type = TREASURE_TYPES[int(choice)-1]
		title = raw_input("Give it a title: ")
		desc = raw_input("Give it a description: ")
		attack = 0
		armor = 0
		if type == 'weapon':
			attack = raw_input("How much damage will it add? [1-999]: ")
			attack = int(attack)
		else:
			armor = raw_input("How much armor will it add? [1-999]: ")
			armor = int(armor)
		tr = Treasure(title=title, description=desc, type=type, armor=armor, attack=attack)
		self.treasures.append(tr)

	def list_treasures(self):
		for treasure in self.treasures:
			print treasure.title

	def save(self):
		f = open("roguey/resources/items.pk", "w")
		pickle.dump(self.treasures, f)
		f.close()

	def main(self):
		while 1:
			print "1. Make a new treasure"
			print "2. List current treasures"
			print "3. Delete a treasure"
			print "4. Edit a treasure"
			print "0. Quit"
			c = raw_input("Make a choice [1-2, 0]: ")
			if c[0] == "1": self.new_treasure()
			if c[0] == "2": self.list_treasures()
			if c[0] == "0": 
				self.save()
				return

if __name__ == "__main__":
	a = Admin()