# INTIALISATION
import pygame, math, sys, random
from pygame.locals import *

class Monster(object):
	def __init__(self):
		pass

	def get_attack(self):
		return self.strength

	def receive_damage(self, damage):
		self.current_hp -= damage


class Derpy(Monster):
	def __init__(self):
		self.title = "Derpy Slime"
		self.level = 1
		self.attack = 10
		self.defense = 1
		self.current_hp = 5
		self.max_hp = 5
		self.strength = 1
		