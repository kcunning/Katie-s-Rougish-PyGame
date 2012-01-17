# INTIALISATION
import pygame, math, sys
from pygame.locals import *

screen = pygame.display.set_mode((1024, 768))
player = pygame.image.load('dude.png')
clock = pygame.time.Clock()
k_up = k_down = k_left = k_right = 0
direction = 0
position = (300, 300)
BLACK = (0,0,0)
WHITE = (255, 255, 255)

def main():
	while 1:
		clock.tick(15)
		hor = 0
		vert = 0
		for event in pygame.event.get():
			if not hasattr(event, 'key'): continue
			if event.key == K_ESCAPE: sys.exit(0)
			if event.key == K_LEFT: hor = -25
			if event.key == K_RIGHT: hor = 25
			if event.key == K_UP: vert = -25
			if event.key == K_DOWN: vert = 25
		x, y = position
		x = x + hor
		y = y + vert
		global position
		position = (x, y)
		screen.fill(BLACK)
		screen.blit(player, position)
		pygame.display.flip()
		


if __name__ == "__main__":
	main()

