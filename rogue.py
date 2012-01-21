# INTIALISATION
import pygame, math, sys, random
from pygame.locals import *

BLACK = (0,0,0)
WHITE = (255, 255, 255)
COLUMNS = 16
ROWS = 21
TREASURES = 10
WALLS = 30
MONSTERS = 3
TILE_SIZE = 48
DIRECTIONS = ['north', 'south', 'east', 'west']
ALL_TREASURES = {
                        "hat": "Quite cunning",
                        "sqord": "Knock-off sword. Probably from Ikea.",
                        "book": "What the hell are you going to do with this?",
			"rainbow": "Joy in a box."
                        }
LONG_STRING = "X" * 50

class Monster(object):
	def __init__(self):
		self.title = "Derp Slime"
		

class Treasure(object):
	''' Not implemented yet. 
	'''
	def __init__(self):
		k = ALL_TREASURES.keys()
		r = random.randint(0, ALL_TREASURES.keys().__len__()-1)
		self.title = ALL_TREASURES.keys()[r]
		self.description = ALL_TREASURES[self.title]

class Map(object):
	''' Stores the values for the map, but doesn't render it for the game. 

	    Map.cleared = The cleared squares
	'''
	def __init__(self):
		''' Sets all squares to uncleared.
		'''
		self.cleared = self.get_blank_map()
		self.current = self.get_blank_map()
		self.treasure = self.get_blank_map()
		self.walls = self.get_blank_map()
		self.monsters = self.get_blank_map()
		for i in range(TREASURES):
			while 1:
				col = random.randint(0, COLUMNS-1)
				row = random.randint(0, ROWS-1)
				if not self.treasure[row][col]:
					self.treasure[row][col] = Treasure()
					break
		for i in range(WALLS):
			while 1:
				col = random.randint(0, COLUMNS-1)
				row = random.randint(0, ROWS-1)
				if not self.treasure[row][col] and not self.walls[row][col]:
					self.walls[row][col] = 1
					break
		for i in range(MONSTERS):
			while 1:
				col = random.randint(0, COLUMNS-1)
				row = random.randint(0, COLUMNS-1)
				if not self.treasure[row][col] and not self.walls[row][col]:
					self.monsters[row][col] = Monster()
					break
			
	def get_blank_map(self):
		''' Returns a map with all values set to 0
		'''
		map = []
		for i in range(ROWS):
                        row = []
                        for j in range(COLUMNS):
                                row.append(0)
                        map.append(row)
		return map
	
	def is_block_empty(self, row, col):
		if not self.treasure[row][col] and not self.monsters[row][col] and not self.walls[row][col]:
			return True
		else:
			return False
	
	def clear_block(self, position):
		''' Given the current position of the player, sets the current square to completely cleared, 
	    	    and the squares nearby to partially cleared.
		'''
		x, y = position
		col = y/TILE_SIZE
		row = x/TILE_SIZE
		
		self.cleared[row][col] = 2
		if row < ROWS-1:
			self.cleared[row+1][col] += 1
		if row > 0:
			self.cleared[row-1][col] += 1
		if col < COLUMNS-1:
			self.cleared[row][col+1] += 1
		if col > 0:
			self.cleared[row][col-1] += 1
	
	def get_all_monsters(self):
		monsters = {}
		for row in range(ROWS):
			for col in range(COLUMNS):
				if self.monsters[row][col]:
					monsters[self.monsters[row][col]] = [row, col]
		return monsters

	def clear_treasure(self, position):
		''' Given a position, clears the treasure from it, and returns the treasure.
		'''	
		x, y = position
		row = x/TILE_SIZE
                col = y/TILE_SIZE
		treasure = self.treasure[row][col]
		self.treasure[row][col] = 0
		return treasure

	def print_ascii_map(self):
		''' Prints an ascii map to the console. For troubleshooting only.
		'''
		for row in self.monsters:
			print row, row.__len__()

	def move_monsters(self):
		monsters = self.get_all_monsters()
		for monster in monsters.keys():
			d = random.sample(DIRECTIONS, 1)[0]
			new_row, new_col = row, col = monsters[monster]
                        if d == "north":
                        	new_row -= 1
                        if d == "south":
                                new_row += 1
                        if d == "east":
                                new_col += 1
                        if d == "west":
                                new_col -= 1
			try:
				if self.is_block_empty(new_row, new_col) and new_row > 0 and new_col > 0:
					self.monsters[new_row][new_col] = monster
					self.monsters[row][col] = 0
			except:
				pass # Monsters can run into walls, edges, chests, etc. It consumes their turn.
					

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

class Game(object):
	''' The game object. Controls rendering the game and moving the player.
	'''
	def __init__(self):
		''' Sets up the initial game board, with the player at a set position.
	    	    Once everything is set up, starts the game.
		'''
		self.screen = pygame.display.set_mode((1280, 832))
		self.font = pygame.font.SysFont(None, 48)
		self.small_font = pygame.font.SysFont(None, 20)
		self.draw_alert("Welcome to Katie's Roguelike!")
		self.inventory = Inventory()
		self.inventory_screen = self.small_font.render("Inventory", True, WHITE, BLACK)
		self.player = pygame.image.load('images/dude.png')
		self.bg = pygame.image.load('images/rainbowbg.png')
		self.clock = pygame.time.Clock()
		self.direction = 0
		self.position = (0, 0)
		self.map = Map()
		self.map.clear_block(self.position)
		treasure = self.map.clear_treasure(self.position)
		if treasure:
			self.add_treasure(treasure)
		self.screen.blit(self.bg, (0,0))
		self.draw_walls()
		self.draw_treasure()
		self.draw_monsters()
		#self.draw_darkness()
		self.draw_inventory()
                self.screen.blit(self.player, self.position)
		self.screen.blit(self.alert, (0, 790))
		self.run()


	def draw_alert(self, alert, color=WHITE):
		''' Draws the alert box at the bottom 
		'''
		self.alert = self.font.render(LONG_STRING, True, BLACK, BLACK)
		self.screen.blit(self.alert, (0, 790))
		try:
			pygame.display.flip()
		except:
			pass
		self.alert = self.font.render(alert, True, color, BLACK)

	def draw_inventory(self):
		self.screen.blit(self.inventory_screen, (1008, 0))
		items = self.inventory.get_items()
		for i in range(items.__len__()):
			line = self.small_font.render(LONG_STRING, True, BLACK, BLACK)
			self.screen.blit(line, (1008, ((i+1)*15)))
		pygame.display.flip()
		for item in items:
			line = self.small_font.render(item, True, WHITE, BLACK)
			self.screen.blit(line, (1008, (items.index(item)+1)*15))
		pygame.display.flip()

	def add_treasure(self, treasure):
		text = "You found a %s. %s" % (treasure.title, treasure.description)
		self.inventory.add_to_inventory(treasure.title)
		self.draw_alert(text)

	def draw_treasure(self):
		''' Draws the treasure chests yet to be opened.
		'''
		for row in range(ROWS):
			for col in range(COLUMNS):
				if self.map.treasure[row][col] != 0:
					treasure = pygame.image.load('images/chest.png')
					self.screen.blit(treasure, (row*TILE_SIZE, col*TILE_SIZE))
	
	def draw_monsters(self):
		for row in range(ROWS):
			for col in range(COLUMNS):
				if self.map.monsters[row][col] != 0:
					monster = pygame.image.load("images/dumb_monster.png")
					self.screen.blit(monster, (row*TILE_SIZE, col*TILE_SIZE))
	
	def draw_walls(self):
		for row in range(ROWS):
			for col in range(COLUMNS):
				if self.map.walls[row][col] != 0:
					wall = pygame.image.load('images/wall.png')
					self.screen.blit(wall, (row*TILE_SIZE, col*TILE_SIZE))

	def draw_darkness(self):
		''' Draws the darkness and shadows on the board. 0 is dark, 1 is in shadows,
	    	    2 is fully revealed.
		'''
		for row in range(ROWS):
			for col in range(COLUMNS):
				if self.map.cleared[row][col] == 0:
					pygame.draw.rect(self.screen, BLACK, (row*TILE_SIZE, col*TILE_SIZE, TILE_SIZE, TILE_SIZE)) 	
				if self.map.cleared[row][col] == 1:
					shadow = pygame.Surface((TILE_SIZE, TILE_SIZE))
					shadow.set_alpha(200)
					shadow.fill(BLACK)
					self.screen.blit(shadow, (row*TILE_SIZE, col*TILE_SIZE))

	def has_wall(self, row, col):
		row = row/TILE_SIZE
		col = col/TILE_SIZE
		if self.map.walls[row][col]:
			return True
		else:
			return False

	def move(self, hor, vert):
		''' Moves the player, given a keypress. 
		'''
		x, y = self.position
		row = x + hor
		col = y + vert
		if row > (ROWS-1) * TILE_SIZE or row < 0 or col > (COLUMNS-1) * TILE_SIZE or col < 0:
			return
		if self.has_wall(row, col):
			return
		self.position = (row, col)
		self.map.clear_block(self.position)
		treasure = self.map.clear_treasure(self.position)
		if treasure:
			self.add_treasure(treasure)
			self.draw_inventory()
		self.screen.blit(self.bg, (0, 0))
		self.draw_treasure()
		self.draw_walls()
		self.draw_monsters()
		#self.draw_darkness()
		self.screen.blit(self.player, self.position)
		self.screen.blit(self.alert, (0, 790))
		pygame.display.flip()

	def run(self):
		''' The main loop of the game.
		'''
		while 1:
			self.clock.tick(30)
			hor = 0
			vert = 0
			for event in pygame.event.get():
                        	if not hasattr(event, 'key'): continue
				if event.type == KEYDOWN:
                        		if event.key == K_ESCAPE: sys.exit(0)
                        		if event.key == K_LEFT: hor = -TILE_SIZE
                        		if event.key == K_RIGHT: hor = TILE_SIZE
                        		if event.key == K_UP: vert = -TILE_SIZE
                        		if event.key == K_DOWN: vert = TILE_SIZE
					self.map.move_monsters()
				self.move(hor, vert)

def main():
        while 1:
		pygame.init()
		game = Game()

if __name__ == "__main__":
        main()

