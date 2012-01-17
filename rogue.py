# INTIALISATION
import pygame, math, sys, random
from pygame.locals import *


BLACK = (0,0,0)
WHITE = (255, 255, 255)
TILES_ACROSS = 21
TILES_DOWN = 16
TREASURES = 3
TILE_SIZE = 48

class Treasure(object):
	''' Not implemented yet. 
	'''
	def __init__(self):
		pass

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
				row = random.randint(0, TILES_ACROSS-1)
				col = random.randint(0, TILES_DOWN-1)
				if not self.treasure[row][col]:
					self.treasure[row][col] = Treasure()
					break
			
		
	def get_blank_map(self):
		''' Returns a map with all values set to 0
		'''
		map = []
		for i in range(TILES_ACROSS):
                        row = []
                        for j in range(TILES_DOWN):
                                row.append(0)
                        map.append(row)
		return map

	def clear_block(self, position):
		''' Given the current position of the player, sets the current square to completely cleared, 
	    	    and the squares nearby to partially cleared.
		'''
		x, y = position
		column = x/TILE_SIZE
		row = y/TILE_SIZE
		self.cleared[column][row] = 2
		if row < TILES_DOWN-1:
			self.cleared[column][row+1] += 1
		if row > 0:
			self.cleared[column][row-1] += 1
		if column < TILES_ACROSS-1:
			self.cleared[column+1][row] += 1
		if column > 0:
			self.cleared[column-1][row] += 1

	def print_ascii_map(self):
		''' Prints an ascii map to the console. For troubleshooting only.
		'''
		for row in self.cleared:
			print row
		
class Game(object):
	''' The game object. Controls rendering the game and moving the player.
	'''
	def __init__(self):
		''' Sets up the initial game board, with the player at a set position.
	    	    Once everything is set up, starts the game.
		'''
		self.screen = pygame.display.set_mode((1024, 768))
		self.player = pygame.image.load('dude.png')
		self.bg = pygame.image.load('boringbg.png')
		self.clock = pygame.time.Clock()
		self.direction = 0
		self.position = (0, 0)
		self.map = Map()
		self.map.clear_block(self.position)
		self.screen.blit(self.bg, (0,0))
		self.draw_treasure()
		self.draw_darkness()
                self.screen.blit(self.player, self.position)
		self.run()

	def draw_treasure(self):
		''' Draws the treasure chests yet to be opened.
		'''
		for row in range(TILES_ACROSS):
			for col in range(TILES_DOWN):
				if self.map.treasure[row][col] != 0:
					treasure = pygame.image.load('chest.png')
					self.screen.blit(treasure, (row*TILE_SIZE, col*TILE_SIZE))

	def draw_darkness(self):
		''' Draws the darkness and shadows on the board. 0 is dark, 1 is in shadows,
	    	    2 is fully revealed.
		'''
		for row in range(TILES_ACROSS):
			for col in range(TILES_DOWN):
				if self.map.cleared[row][col] == 0:
					pygame.draw.rect(self.screen, BLACK, (row*TILE_SIZE, col*TILE_SIZE, TILE_SIZE, TILE_SIZE)) 	
				if self.map.cleared[row][col] == 1:
					shadow = pygame.Surface((TILE_SIZE, TILE_SIZE))
					shadow.set_alpha(200)
					shadow.fill(BLACK)
					self.screen.blit(shadow, (row*TILE_SIZE, col*TILE_SIZE))

	def move(self, hor, vert):
		''' Moves the player, given a keypress. If the player hits ESC, the game quits.
		'''
		x, y = self.position
		x = x + hor
		y = y + vert
		if x > (TILES_ACROSS-1) * TILE_SIZE or x < 0 or y > (TILES_DOWN-1) * TILE_SIZE or y < 0:
			return
		self.position = (x, y)
		self.map.clear_block(self.position)
		self.screen.blit(self.bg, (0, 0))
		self.draw_treasure()
		self.draw_darkness()
		self.screen.blit(self.player, self.position)
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
		game = Game()

if __name__ == "__main__":
        main()

