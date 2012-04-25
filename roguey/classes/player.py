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

    def add_to_inventory(self, item, player):
        ''' Adds an item to the inventory
        '''
        if item.item_type == "trash":
            return
        if player.equipped[item.item_type ]:
            try:
                self.inventory[item] += 1
            except:
                self.inventory[item] = 1
        else:
            player.equip_item(item)


class Player(object):
    """The player class. Contains level, HP, stats, and deals with combat."""
    def __init__(self):
        self.level = 1
        self.stats = {
            'strength': 1,
            'attack': 1,
            'defense': 5
        }
        self.current_hp = 10
        self.name = "Dudeguy McAwesomesauce"
        self.equipped = {}

        for treasure in EQUIPMENT_TYPES:
            self.equipped[treasure] = None

    @property
    def max_hp(self):
        return 10 + (self.level-1)*5

    @property
    def defense(self):
        return self.stats['defense'] + self.get_armor()

    def get_armor(self):
        armor = 0
        for slot in self.equipped.keys():
            try:
                armor += self.equipped[slot].armor
            except:
                pass
        return armor

    def receive_damage(self, damage):
        self.current_hp -= damage

    def attempt_block(self, attack):
        pass

    @property
    def attack(self):
        atk = 0
        if self.equipped['hands']:
            atk += self.equipped['hands'].attack
        return self.stats['attack'] + atk

    def equip_item(self, item):
        self.equipped[item.item_type] = item


        