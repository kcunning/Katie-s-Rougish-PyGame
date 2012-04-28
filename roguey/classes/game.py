import pygame, sys, pickle
from pygame.locals import *

from constants import *
from items import Treasure
from gamemap import Map
from monsters import Derpy
from player import Inventory, Player
from combat import Combat
from gamescreen import GameScreen

class Game(object):
    ''' The game object. Controls rendering the game and moving the player.
    '''
    def __init__(self):
        ''' Sets up the initial game board, with the player at a set position.
                Once everything is set up, starts the game.
        '''
        # Set up the screen
        self.screen = GameScreen()
        self.bg = pygame.image.load(IMG_DIR + 'rainbowbg.png')

        # Set up some game components
        self.inventory = Inventory()
        self.map = Map()
        self.map.player = (1*TILE_SIZE, 1*TILE_SIZE)
        self.player_stats = Player()
        treasure = self.map.clear_treasure(self.map.player)
        if treasure:
            self.add_treasure(treasure)

        self.clock = pygame.time.Clock()
        self.direction = 0
        
        self.map.clear_block(self.map.player)
        self.map.set_current_position(self.map.player)

        self.screen.draw_screen_layers(player_stats=self.player_stats, map=self.map)
        
        self.run()

    def add_treasure(self, treasure):
        ''' Adds the treasure to the player's inventory
        '''
        text = "You found a %s. %s" % (treasure.title, treasure.description)
        self.inventory.add_to_inventory(treasure, self.player_stats)
        self.screen.draw_alert(text)

    def move(self, hor, vert):
        ''' Moves the player, given a keypress. 
            Also evaluates if the player needs to fight or pick up some treasure.
        '''
        self.old_row, self.old_col = self.map.player
        row = self.old_row + hor
        col = self.old_col + vert
        if row > (ROWS-1) * TILE_SIZE or row < 0 or col > (COLUMNS-1) * TILE_SIZE or col < 0:
            return
        if self.map.has_wall(row, col):
            return
        if self.map.has_monster(row, col):
            Combat(self.player_stats, self.map.monsters[row/TILE_SIZE][col/TILE_SIZE])
            if self.map.monsters[row/TILE_SIZE][col/TILE_SIZE].current_hp <= 0:
                pass #put death throes here
            if self.player_stats.current_hp <= 0:
                self.end_game()
            self.move(0,0)
            return
        self.map.player = (row, col)
        self.map.player = (row, col)
        self.map.clear_block(self.map.player)
        self.map.set_current_position(self.map.player)
        treasure = self.map.clear_treasure(self.map.player)
        if treasure:
            self.add_treasure(treasure)
            self.screen.draw_inventory(self.inventory)
            self.screen.draw_equipment(self.player_stats.equipped)

    def refresh_screen(self):
        self.screen.draw_player(self.map.player)
        self.screen.draw_screen_layers(self.map, self.player_stats)

    def end_game(self):
        ''' The exit screen for when the player has died, or completed the game. 
            So far, all it does is exit the game.
        '''
        sys.exit()

    def run(self):
        ''' The main loop of the game.
        '''
        # Fix for double move from Joshua Grigonis! Thanks!
        hor = 0
        vert = 0
        while 1:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE: 
                        sys.exit(0)
                    if event.key == K_LEFT:
                        hor = -TILE_SIZE
                        vert = 0
                    if event.key == K_RIGHT:
                        hor = TILE_SIZE
                        vert = 0
                    if event.key == K_UP:
                        vert = -TILE_SIZE
                        hor = 0
                    if event.key == K_DOWN:
                        vert = TILE_SIZE
                        hor = 0
                if event.type == KEYUP:
                    # updates only occur is player has moved.
                    if vert or hor:
                        self.move(hor, vert)
                        self.map.move_monsters()
                        hor = 0
                        vert = 0    
            self.refresh_screen()