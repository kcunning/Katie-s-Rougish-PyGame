from os.path import abspath, dirname, join, sep

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
LONG_STRING = "X" * 50

EQUIPMENT_TYPES = ('hat', 'shirt', 'pants', 'shoes', 'back', 'neck', 'hands', 'weapon')
START_EQUIPMENT = {}
for treasure in EQUIPMENT_TYPES:
	START_EQUIPMENT[treasure] = None

TREASURE_TYPES = ('hat', 'shirt', 'pants', 'shoes', 'back', 'neck', 'hands', 'weapon', 'trash')

IMG_DIR = join(
	dirname(dirname(abspath(__file__))),
	"images"
	) + sep

STATS = ('strength', 'attack', 'defense')
