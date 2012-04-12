# INTIALISATION
import pygame, math, sys, random
from pygame.locals import *

from constants import *

class Treasure(object):
    ''' Not implemented yet. 
    '''
    def __init__(self, title="Nada", description="", type="trash", armor=0, buff=0, attack=0):
        self.title = title
        self.description = description
        self.type = type
        self.armor = armor
        self.buff = buff
        self.attack = attack

