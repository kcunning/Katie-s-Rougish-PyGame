# INTIALISATION
import pygame, math, sys
from pygame.locals import *


BLACK = (0,0,0)
WHITE = (255, 255, 255)
TILES_ACROSS = 20 - 1
TILES_DOWN = 15 - 1

class Map(object):
	def __init__(self):
		self.map = []
		for i in range(TILES_ACROSS+1):
			row = []
			for j in range(TILES_DOWN+1):
				row.append(0)
			self.map.append(row)

	def clear_block(self, position):
		x, y = position
		column = x/50
		row = y/50
		self.map[column][row] = 1

	def print_ascii_map(self):
		for row in self.map:
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
		self.map.print_ascii_map()
		self.screen.blit(self.bg, (0,0))
		self.draw_darkness()
                self.screen.blit(self.player, self.position)
		self.run()

	def draw_darkness(self):
		for row in range(TILES_ACROSS+1):
			for col in range(TILES_DOWN+1):
				if self.map.map[row][col] == 0:
					pygame.draw.rect(self.screen, BLACK, (row*50, col*50, 50, 50)) 	

	def move(self, hor, vert):
		x, y = self.position
		x = x + hor
		y = y + vert
		if x > TILES_ACROSS * 50 or x < 0 or y > TILES_DOWN * 50 or y < 0:
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

