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
        self.current_hp = 10
        self.strength = 1
        self.name = "Dudeguy McAwesomesauce"

    @property
    def max_hp(self):
        return 10 + (self.level-1)*5

    @property
    def defense(self):
        return 1

    def receive_damage(self, damage):
        pass

    def attempt_block(self, attack):
        pass

    def attack(self, attack):
        pass


        