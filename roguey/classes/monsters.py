# INTIALISATION
import pygame, math, sys, random
from pygame.locals import *

class Monster(object):
	def __init__(self):
		pass

class Derpy(Monster):
	def __init__(self):
		self.title = "Derpy Slime"
		self.level = 1
		self.attack = 1
		self.defence = 1
		self.max_hq = 5
		self.max_hp = 5
		