import pygame, sys
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
        self.screen.draw_alert("Welcome to Katie's Roguelike!")
        self.bg = pygame.image.load(IMG_DIR + 'rainbowbg.png')

        # Set up some game components
        self.inventory = Inventory()
        self.map = Map()
        self.map.player = (0, 0)
        self.player_stats = Player()
        treasure = self.map.clear_treasure(self.map.player)
        if treasure:
            self.add_treasure(treasure)

        self.clock = pygame.time.Clock()
        self.direction = 0
        
        self.map.clear_block(self.map.player)
        self.map.set_current_position(self.map.player)
        
        self.screen.draw_walls(self.map.walls)
        self.screen.draw_stats(player_stats=self.player_stats)
        self.screen.draw_treasure(self.map.treasure)
        self.screen.draw_monsters(self.map)
        self.screen.draw_darkness(self.map)
        self.screen.draw_inventory(self.inventory)
        self.screen.draw_stats(player_stats=self.player_stats)
        self.run()

    def add_treasure(self, treasure):
        text = "You found a %s. %s" % (treasure.title, treasure.description)
        self.inventory.add_to_inventory(treasure.title)
        self.screen.draw_alert(text)

    def has_wall(self, row, col):
        row = row/TILE_SIZE
        col = col/TILE_SIZE
        if self.map.walls[row][col]:
            return True
        else:
            return False

    def has_monster(self, row, col):
        row = row/TILE_SIZE
        col = col/TILE_SIZE
        if self.map.monsters[row][col]:
            return True
        else:
            return False
    

    def move(self, hor, vert):
        ''' Moves the player, given a keypress. 
        '''
        self.old_row, self.old_col = self.map.player
        row = self.old_row + hor
        col = self.old_col + vert
        if row > (ROWS-1) * TILE_SIZE or row < 0 or col > (COLUMNS-1) * TILE_SIZE or col < 0:
            return
        if self.has_wall(row, col):
            return
        if self.has_monster(row, col):
            Combat(self.player_stats, self.map.monsters[row/TILE_SIZE][col/TILE_SIZE]).fight()
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
        self.screen.draw_player(self.map.player)
        self.draw_screen_layers()
        self.screen.draw_player(self.map.player)
        #self.screen.blit(self.player_blit, self.map.player)
        pygame.display.flip()

    def end_game(self):
        sys.exit()

    def draw_screen_layers(self):
        self.screen.draw_background()
        self.screen.draw_treasure(self.map.treasure)
        self.screen.draw_walls(self.map.walls)
        self.screen.draw_monsters(self.map)
        self.screen.draw_darkness(self.map)
        self.screen.draw_stats(player_stats=self.player_stats)

    def run(self):
        ''' The main loop of the game.
        '''
        # Fix for double move from Joshua Grigonis! Thanks!
        hor = 0
        vert = 0
        while 1:
            self.clock.tick(30)
            for event in pygame.event.get():
                if not hasattr(event, 'key'): 
                    continue
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
                    self.move(hor, vert)
                    self.map.move_monsters()
                    hor = 0
                    vert = 0
