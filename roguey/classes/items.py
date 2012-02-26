# INTIALISATION
import pygame, math, sys, random
from pygame.locals import *

from constants import *

class Treasure(object):
    ''' Not implemented yet. 
    '''
    def __init__(self):
        self.title = random.choice(ALL_TREASURES.keys())
        self.description = ALL_TREASURES[self.title]
