from player import Player
from monsters import Derpy

from random import randint

class Combat(object):

	def __init__(self, player, monster):
		self.player = player
		self.monster = monster

	def fight(self):
		'''For now, we'll always start with the player.'''
		# Player, try to hit the monster!
		hit_attempt = randint(0, self.player.attack)
		if hit_attempt == 0:
			print "A wiff!"
		if hit_attempt > 0 and hit_attempt <= self.monster.defense:
			print "It barely misses."
		if hit_attempt > self.monster.defense:
			damage = self.player.get_attack()
			self.monster.receive_damage(damage)
			if self.monster.current_hp <= 0:
				self.kill_monster()
				return
			print self.monster.current_hp
		# Monster, try to hit back.

		hit_attempt = randint(0, self.monster.attack)
		if hit_attempt == 0:
			print "Monster wiffs!"
		if hit_attempt > 0 and hit_attempt <= self.player.defense:
			print "Monster barely misses", str(hit_attempt)
		if hit_attempt > self.player.defense:
			damage = self.monster.get_attack()
			self.player.receive_damage(damage)

	def kill_monster(self):
		self.monster = None
