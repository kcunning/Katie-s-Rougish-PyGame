from os.path import abspath, dirname

MOVEMENT_SIZE = 12
RADIUS = 2
BLACK = (0,0,0)
WHITE = (255, 255, 255)
COLUMNS = 16
ROWS = 21
TREASURES = 10
MAX_ROOMS = 10
MONSTERS = 12
TILE_SIZE = 48
DIRECTIONS = ['north', 'south', 'east', 'west']
ALL_TREASURES = {
                "hat": "Quite cunning",
                "sqord": "Knock-off sword. Probably from Ikea.",
                "book": "What the hell are you going to do with this?",
                "rainbow": "Joy in a box."
                }
LONG_STRING = "X" * 50

TREASURE_TYPES = ('hat', 'shirt', 'pants', 'shoes', 'back', 'neck', 'hands', 'weapon', 'trash')

IMG_DIR = dirname(dirname(abspath(__file__))) + "/images/"
