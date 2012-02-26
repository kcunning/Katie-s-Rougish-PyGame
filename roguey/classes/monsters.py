# INTIALISATION
import pygame, math, sys, random
from pygame.locals import *

class Monster(object):
	def __init__(self):
		pass
		self.in_combat = False

class Derpy(Monster):
	def __init__(self):
		self.title = "Derpy Slime"
		self.level = 1
		