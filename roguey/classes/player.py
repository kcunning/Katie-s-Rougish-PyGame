class Inventory(object):
	''' The inventory for the player.
	'''

	def __init__(self):
		''' Sets up the initial blank inventory.
		'''
		self.inventory = {}

	def get_items(self):
		return self.inventory.keys()

	def add_to_inventory(self, item):
		''' Adds an item to the inventory
		'''
		try:
			self.inventory[item] += 1
		except:
			self.inventory[item] = 1
