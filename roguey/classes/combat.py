from player import Player
from monsters import Derpy

from random import randint

class Combat(object):

	def __init__(self, player, monster):
		self.player = player
		self.monster = monster
		self.fight()

	def fight(self):
		'''For now, we'll always start with the player.'''
		# Player, try to hit the monster!
		hit_attempt = randint(0, self.player.attack)
		if hit_attempt > self.monster.defense:
			damage = self.player.strength
			self.monster.receive_damage(damage)

		# Monster, try to hit back.
		if self.monster.current_hp > 0:
			hit_attempt = randint(0, self.monster.attack)
			if hit_attempt > self.player.defense:
				damage = self.monster.strength
				self.player.receive_damage(damage)