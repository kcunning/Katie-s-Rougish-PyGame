# INTIALISATION
import pygame, math, sys, random
from pygame.locals import *

from constants import *

class Treasure(object):
	''' Not implemented yet. 
	'''
	def __init__(self):
		k = ALL_TREASURES.keys()
		r = random.randint(0, ALL_TREASURES.keys().__len__()-1)
		self.title = ALL_TREASURES.keys()[r]
		self.description = ALL_TREASURES[self.title]
