import pygame, math, sys, random
from pygame.locals import *

sys.path.append("roguey/classes")

from constants import *
from items import Treasure
from gamemap import Map
from monsters import Monster
from player import Inventory
from game import Game

def main():
    while 1:
        pygame.init()
        game = Game()

if __name__ == "__main__":
        main()
