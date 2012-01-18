# INTIALISATION
import pygame, math, sys, random
from pygame.locals import *

BLACK = (0,0,0)
WHITE = (255, 255, 255)
COLUMNS = 21
ROWS = 16
TREASURES = 4
TILE_SIZE = 48
ALL_TREASURES = {
                        "hat": "Quite cunning",
                        "sqord": "Knock-off sword. Probably from Ikea.",
                        "book": "What the hell are you going to do with this?"
                        }

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
		self.treasure = self.get_blank_map()
		for i in range(TREASURES):
			while 1:
				col = random.randint(0, COLUMNS-1)
				row = random.randint(0, ROWS-1)
				if not self.treasure[row][col]:
					self.treasure[row][col] = Treasure()
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
		print map.__len__(), map[0].__len__()
		return map

	def clear_block(self, position):
		''' Given the current position of the player, sets the current square to completely cleared, 
	    	    and the squares nearby to partially cleared.
		'''
		x, y = position
		col = y/TILE_SIZE
		row = x/TILE_SIZE
		print "Row: %s, Col: %s" % (str(row), str(col))
		
		self.cleared[row][col] = 2
		if row < ROWS-1:
			self.cleared[row+1][col] += 1
		if row > 0:
			self.cleared[row-1][col] += 1
		if col < COLUMNS-1:
			self.cleared[row][col+1] += 1
		if col > 0:
			self.cleared[row][col-1] += 1
	
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
		for row in self.cleared:
			print row, row.__len__()
		
class Game(object):
	''' The game object. Controls rendering the game and moving the player.
	'''
	def __init__(self):
		''' Sets up the initial game board, with the player at a set position.
	    	    Once everything is set up, starts the game.
		'''
		self.font = pygame.font.SysFont(None, 48)
		self.alert = self.font.render("Welcome to Katie's Roguelike!", True, WHITE, BLACK)
		self.treasures = []
		self.screen = pygame.display.set_mode((1280, 832))
		self.player = pygame.image.load('dude.png')
		self.bg = pygame.image.load('rainbowbg.png')
		self.clock = pygame.time.Clock()
		self.direction = 0
		self.position = (0, 0)
		self.map = Map()
		self.map.clear_block(self.position)
		treasure = self.map.clear_treasure(self.position)
		if treasure:
			add_treasure(treasure)
		self.screen.blit(self.bg, (0,0))
		self.draw_treasure()
		self.draw_darkness()
                self.screen.blit(self.player, self.position)
		self.screen.blit(self.alert, (0, 790))
		self.map.print_ascii_map()
		self.run()

	def add_treasure(self, treasure):
		self.treasures.append(treasure)
		text = "You found a %s. %s" % (treasure.title, treasure.description)
		self.alert = self.font.render(text, True, WHITE, BLACK)

	def draw_treasure(self):
		''' Draws the treasure chests yet to be opened.
		'''
		for row in range(ROWS):
			for col in range(COLUMNS):
				if self.map.treasure[row][col] != 0:
					treasure = pygame.image.load('chest.png')
					self.screen.blit(treasure, (row*TILE_SIZE, col*TILE_SIZE))

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

	def move(self, hor, vert):
		''' Moves the player, given a keypress. 
		'''
		print hor, vert
		x, y = self.position
		row = x + hor
		col = y + vert
		if row > (ROWS-1) * TILE_SIZE or row < 0 or col > (COLUMNS-1) * TILE_SIZE or col < 0:
			return
		self.position = (row, col)
		self.map.clear_block(self.position)
		treasure = self.map.clear_treasure(self.position)
		if treasure:
			self.add_treasure(treasure)
		self.screen.blit(self.bg, (0, 0))
		self.draw_treasure()
		self.draw_darkness()
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
                        	if event.key == K_ESCAPE: sys.exit(0)
                        	if event.key == K_LEFT: hor = -TILE_SIZE/2
                        	if event.key == K_RIGHT: hor = TILE_SIZE/2
                        	if event.key == K_UP: vert = -TILE_SIZE/2
                        	if event.key == K_DOWN: vert = TILE_SIZE/2
				self.move(hor, vert)

def main():
        while 1:
		pygame.init()
		game = Game()

if __name__ == "__main__":
        main()

