# INTIALISATION
import pygame, math, sys, random
from pygame.locals import *

from constants import *
from items import Treasure
from monsters import Monster

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
	
	def set_current_position(self, position):
		self.cleared = self.get_blank_map()
		row, col = position
		self.cleared[row][col] = 1

	def clear_block(self, position):
		''' Given the current position of the player, sets the current square to completely cleared, 
	    	    and the squares nearby to partially cleared.
		'''
		x, y = position
		col = y/TILE_SIZE
		row = x/TILE_SIZE
		
		self.cleared[row][col] = 1
		if row < ROWS-1:
			self.cleared[row+1][col] = 1
		if row > 0:
			self.cleared[row-1][col] = 1
		if col < COLUMNS-1:
			self.cleared[row][col+1] = 1
		if col > 0:
			self.cleared[row][col-1] = 1
	
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
