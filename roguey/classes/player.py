from constants import *

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


class Player(object):
    """The player class. Contains level, HP, stats, and deals with combat."""
    def __init__(self):
        self.level = 1
        self.attack = 5
        self.defense = 5
        self.current_hp = 10
        self.strength = 1
        self.name = "Dudeguy McAwesomesauce"
        self.equipped = {}

        for treasure in TREASURE_TYPES:
            self.equipped[treasure] = None

    @property
    def max_hp(self):
        return 10 + (self.level-1)*5

    @property
    def get_defense(self):
        return 1

    def receive_damage(self, damage):
        self.current_hp -= damage

    def attempt_block(self, attack):
        pass

    def get_attack(self):
        return self.strength


        