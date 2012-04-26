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

    @property
    def strength(self):
        return self.stats['strength']

    def get_armor(self):
        armor = 0
        for slot in self.equipped.keys():
            if self.equipped[slot]:
                try:
                    armor += self.equipped[slot].armor
                except AttributeError:
                    # The Treasure in this slot doesn't have an 'armor' attribute
                    pass
                except TypeError:
                    # The Treasure in this slot has an armor stat, however it
                    # appears to be a non numeric type. Make sure this Treasures armor stat
                    # has the attribute type="int" in its XML definition.
                    # This sort of error should probably get properly logged somewhere
                    print (
                        'Please make sure the armor stat for the "%s" weapon '
                        'has the type="int" attribute in its XML definition' % self.equipped[slot].title
                    )

        return armor

    def receive_damage(self, damage):
        self.current_hp -= damage

    def attempt_block(self, attack):
        pass

    @property
    def attack(self):
        atk = 0
        if self.equipped['weapon']:
            try:
                atk += self.equipped['weapon'].damage
            except AttributeError:
                # This weapon does not have a "damage" attribute. This may not
                # be an error; it may just suck.
                pass
            except TypeError:
                # The weapon has a damage attribute, however it
                # appears to be non numeric type. Make sure this damage stat
                # has the attribute type="int" in its XML definition.
                # This sort of error should probably get properly logged somewhere
                print (
                    'Please make sure the armor stat for the "%s" weapon '
                    'has the type="int" attribute in its XML definition' % self.equipped['weapon'].title
                )
        return self.stats['attack'] + atk

    def equip_item(self, item):
        self.equipped[item.item_type] = item


        