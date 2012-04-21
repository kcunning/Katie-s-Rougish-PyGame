# INTIALISATION
import pygame, math, sys, random
from pygame.locals import *

class Monster(object):
	def __init__(self):
		pass

	@property
	def attack(self):
		return self.stats['attack']

	def receive_damage(self, damage):
		self.current_hp -= damage

	@property
	def defense(self):
		return self.stats['defense']

	@property
	def strength(self):
		return self.stats['strength']

class Derpy(Monster):
	def __init__(self):
		self.title = "Derpy Slime"
		self.level = 1
		self.stats ={
			'attack': 10,
			'defense': 1,
			'strength': 1,
		}
		self.current_hp = 5
		self.max_hp = 5
		