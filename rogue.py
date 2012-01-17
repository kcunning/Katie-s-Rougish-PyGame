# INTIALISATION
import pygame, math, sys
from pygame.locals import *


BLACK = (0,0,0)
WHITE = (255, 255, 255)
TILES_ACROSS = 20
TILES_DOWN = 15

class Treasure(object):
	def __init__(self):
		pass

class Map(object):
	def __init__(self):
		self.cleared = self.get_blank_map()
		
	def get_blank_map(self):
		map = []
		for i in range(TILES_ACROSS):
                        row = []
                        for j in range(TILES_DOWN):
                                row.append(0)
                        map.append(row)
		return map

	def clear_block(self, position):
		x, y = position
		column = x/50
		row = y/50
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
		for row in self.cleared:
			print row
		
class Game(object):
	def __init__(self):
		self.screen = pygame.display.set_mode((1024, 768))
		self.player = pygame.image.load('dude.png')
		self.bg = pygame.image.load('rainbowbg.png')
		self.clock = pygame.time.Clock()
		self.direction = 0
		self.position = (300, 300)
		self.map = Map()
		self.map.clear_block(self.position)
		self.screen.blit(self.bg, (0,0))
		self.draw_darkness()
                self.screen.blit(self.player, self.position)
		self.run()

	def draw_darkness(self):
		for row in range(TILES_ACROSS):
			for col in range(TILES_DOWN):
				if self.map.cleared[row][col] == 0:
					pygame.draw.rect(self.screen, BLACK, (row*50, col*50, 50, 50)) 	
				if self.map.cleared[row][col] == 1:
					shadow = pygame.Surface((50,50))
					shadow.set_alpha(200)
					shadow.fill(BLACK)
					self.screen.blit(shadow, (row*50, col*50))

	def move(self, hor, vert):
		x, y = self.position
		x = x + hor
		y = y + vert
		if x > (TILES_ACROSS-1) * 50 or x < 0 or y > (TILES_DOWN-1) * 50 or y < 0:
			return
		self.position = (x, y)
		self.map.clear_block(self.position)
		self.screen.blit(self.bg, (0, 0))
		self.draw_darkness()
		self.screen.blit(self.player, self.position)
		pygame.display.flip()

	def run(self):
		while 1:
			self.clock.tick(30)
			hor = 0
			vert = 0
			for event in pygame.event.get():
                        	if not hasattr(event, 'key'): continue
                        	if event.key == K_ESCAPE: sys.exit(0)
                        	if event.key == K_LEFT: hor = -25
                        	if event.key == K_RIGHT: hor = 25
                        	if event.key == K_UP: vert = -25
                        	if event.key == K_DOWN: vert = 25
				self.move(hor, vert)

def main():
        while 1:
		game = Game()

if __name__ == "__main__":
        main()

