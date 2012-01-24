import pygame, sys
from pygame.locals import *

from constants import *
from items import Treasure
from gamemap import Map
from monsters import Monster
from player import Inventory

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
		self.player = pygame.image.load(IMG_DIR + 'dude.png')
		self.bg = pygame.image.load(IMG_DIR + 'rainbowbg.png')
		self.clock = pygame.time.Clock()
		self.direction = 0
		self.position = (0, 0)
		self.map = Map()
		self.map.clear_block(self.position)
		self.map.set_current_position(self.position)
		treasure = self.map.clear_treasure(self.position)
		if treasure:
			self.add_treasure(treasure)
		self.screen.blit(self.bg, (0,0))
		self.draw_walls()
		self.draw_treasure()
		self.draw_monsters()
		self.draw_darkness()
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
					treasure = pygame.image.load(IMG_DIR + 'chest.png')
					self.screen.blit(treasure, (row*TILE_SIZE, col*TILE_SIZE))
	
	def draw_monsters(self):

		

		for row in range(ROWS):
			for col in range(COLUMNS):
				if self.map.monsters[row][col] != 0 and self.map.current[row][col] != 0:
					monster = pygame.image.load(IMG_DIR + 'dumb_monster.png')
					self.screen.blit(monster, (row*TILE_SIZE, col*TILE_SIZE))
	
	def draw_walls(self):
		for row in range(ROWS):
			for col in range(COLUMNS):
				if self.map.walls[row][col] != 0:
					wall = pygame.image.load(IMG_DIR + 'wall.png')
					self.screen.blit(wall, (row*TILE_SIZE, col*TILE_SIZE))

	def draw_darkness(self):
		''' Draws the darkness and shadows on the board. 0 is dark, 1 is in shadows,
		'''
		for row in range(ROWS):
			for col in range(COLUMNS):
				if self.map.cleared[row][col] == 0:
					if not self.map.current[row][col]:
						pygame.draw.rect(self.screen, BLACK, (row*TILE_SIZE, col*TILE_SIZE, TILE_SIZE, TILE_SIZE)) 	
				if self.map.cleared[row][col] == 1:
					if not self.map.current[row][col]:
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
		self.old_row, self.old_col = self.position
		row = self.old_row + hor
		col = self.old_col + vert
		if row > (ROWS-1) * TILE_SIZE or row < 0 or col > (COLUMNS-1) * TILE_SIZE or col < 0:
			return
		if self.has_wall(row, col):
			return
		self.position = (row, col)
		self.map.clear_block(self.position)
		self.map.set_current_position(self.position)
		treasure = self.map.clear_treasure(self.position)
		if treasure:
			self.add_treasure(treasure)
			self.draw_inventory()
		self.animate_move(hor, vert, "player")
		self.draw_screen_layers()
		self.screen.blit(self.player, self.position)
		pygame.display.flip()

	def draw_screen_layers(self):
		self.screen.blit(self.bg, (0, 0))
                self.draw_treasure()
                self.draw_walls()
                self.draw_monsters()
                self.draw_darkness()
		self.screen.blit(self.alert, (0, 790))

	def animate_move(self, hor, vert, blit):
		if vert:
                        if vert > 0:
                                for i in range(TILE_SIZE/MOVEMENT_SIZE):
                                        self.draw_screen_layers()
                                        self.screen.blit(self.__getattribute__(blit), [self.old_row, self.old_col+i*MOVEMENT_SIZE])
                                        pygame.display.update()
                        else:
                                for i in range(TILE_SIZE/MOVEMENT_SIZE):
                                        self.draw_screen_layers()
                                        self.screen.blit(self.__getattribute__(blit), [self.old_row, self.old_col-i*MOVEMENT_SIZE])
                                        pygame.display.update()
                if hor:
                        if hor > 0:
                                for i in range(TILE_SIZE/MOVEMENT_SIZE):
                                        self.draw_screen_layers()
                                        self.screen.blit(self.__getattribute__(blit), [self.old_row+i*MOVEMENT_SIZE, self.old_col])
                                        pygame.display.update()
                        else:
                                for i in range(TILE_SIZE/MOVEMENT_SIZE):
                                        self.draw_screen_layers()
                                        self.screen.blit(self.__getattribute__(blit), [self.old_row-i*MOVEMENT_SIZE, self.old_col])
                                        pygame.display.update()


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
