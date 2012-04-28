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

	def __str__(self):
		return (
			"%s | Level %d | HP (%d/%d) | attack %d | defense %d | strength %d" %
			(
				self.title,
				self.level,
				self.current_hp,
				self.max_hp,
				self.stats['attack'],
				self.stats['defense'],
				self.stats['strength']
				)
			)

class Derpy(Monster):
	def __init__(self):
		self.title = "Derpy Slime"
		self.level = 1
		self.stats ={
			'attack': 5,
			'defense': 1,
			'strength': 1,
		}
		self.current_hp = 3
		self.max_hp = 3
		
class RatBird(Monster):
	def __init__(self):
		self.title = "Ratbird"
		self.level = 2
		self.stats = {
			'attack': 7,
			'defense': 2,
			'strength': 2,
		}
		self.max_hp = 5
		self.current_hp = self.max_hp