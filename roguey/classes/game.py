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
        self.screen.draw_inventory()
        self.screen.draw_stats()
        self.screen.blit(self.player_blit, self.map.player)
        self.screen.blit(self.alert, (0, 790))
        self.run()

    def draw_stats(self, color=WHITE):
        self.screen.blit(self.stats_screen, (1008, 0))
        self.stats_screen = self.small_font.render(self.player_stats.name, True, color, BLACK)
        self.screen.blit(self.stats_screen, (1008, 0))
        self.stats_screen = self.small_font.render("Level: " + str(self.player_stats.level), True, color, BLACK)
        self.screen.blit(self.stats_screen, (1008, 15))
        self.stats_screen = self.small_font.render("HP: %s/%s" % (str(self.player_stats.current_hp), str(self.player_stats.max_hp)), True, color, BLACK)
        self.screen.blit(self.stats_screen, (1008, 30)) 

    def draw_alert(self, alert, color=WHITE):
        ''' Draws the alert box at the bottom 
        '''
        self.alert = self.font.render(LONG_STRING, True, BLACK, BLACK)
        self.screen.blit(self.alert, (0, 790))
        try:
            pygame.display.flip()
        except:
            pass
        self.alert = self.font.render(alert, True, color, BLACK)

    def draw_inventory(self):
        self.screen.blit(self.inventory_screen, (1008, 100))
        items = self.inventory.get_items()
        for i in range(items.__len__()):
            line = self.small_font.render(LONG_STRING, True, BLACK, BLACK)
            self.screen.blit(line, (1008, ((i+1)*15)+100))
        pygame.display.flip()
        for item in items:
            line = self.small_font.render(item, True, WHITE, BLACK)
            self.screen.blit(line, (1008, (items.index(item)+1)*15+100))
        pygame.display.flip()

    def add_treasure(self, treasure):
        text = "You found a %s. %s" % (treasure.title, treasure.description)
        self.inventory.add_to_inventory(treasure.title)
        self.draw_alert(text)

    def draw_treasure(self):
        ''' Draws the treasure chests yet to be opened.
        '''
        for row in range(ROWS):
            for col in range(COLUMNS):
                if self.map.treasure[row][col] != 0:
                    treasure = pygame.image.load(IMG_DIR + 'chest.png')
                    self.screen.blit(treasure, (row*TILE_SIZE, col*TILE_SIZE))
    
    def draw_monsters(self):
        for row in range(ROWS):
            for col in range(COLUMNS):
                if self.map.monsters[row][col] != 0 and self.map.current[row][col] != 0:
                    monster = pygame.image.load(IMG_DIR + 'dumb_monster.png')
                    self.screen.blit(monster, (row*TILE_SIZE, col*TILE_SIZE))

    def draw_darkness(self):
        ''' Draws the darkness and shadows on the board. 0 is dark, 1 is in shadows,
        '''
        for row in range(ROWS):
            for col in range(COLUMNS):
                if self.map.cleared[row][col] == 0:
                    if not self.map.current[row][col]:
                        pygame.draw.rect(self.screen, BLACK, (row*TILE_SIZE, col*TILE_SIZE, TILE_SIZE, TILE_SIZE))  
                if self.map.cleared[row][col] == 1:
                    if not self.map.current[row][col]:
                        shadow = pygame.Surface((TILE_SIZE, TILE_SIZE))
                        shadow.set_alpha(200)
                        shadow.fill(BLACK)
                        self.screen.blit(shadow, (row*TILE_SIZE, col*TILE_SIZE))

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
            self.draw_inventory()
        self.screen.blit(self.player_blit, self.map.player)
        self.draw_screen_layers()
        self.screen.blit(self.player_blit, self.map.player)
        pygame.display.flip()

    def end_game(self):
        sys.exit()

    def draw_screen_layers(self):
        self.screen.blit(self.bg, (0, 0))
        self.draw_treasure()
        self.draw_walls()
        self.draw_monsters()
        self.draw_darkness()
        self.draw_stats()
        self.screen.blit(self.alert, (0, 790))

    def animate_move(self, hor, vert, blit):
        if vert:
            if vert > 0:
                for i in range(TILE_SIZE/MOVEMENT_SIZE):
                    self.draw_screen_layers()
                    self.screen.blit(self.__getattribute__(blit), [self.old_row, self.old_col+i*MOVEMENT_SIZE])
                    pygame.display.update()
            else:
                for i in range(TILE_SIZE/MOVEMENT_SIZE):
                    self.draw_screen_layers()
                    self.screen.blit(self.__getattribute__(blit), [self.old_row, self.old_col-i*MOVEMENT_SIZE])
                    pygame.display.update()
        if hor:
            if hor > 0:
                for i in range(TILE_SIZE/MOVEMENT_SIZE):
                    self.draw_screen_layers()
                    self.screen.blit(self.__getattribute__(blit), [self.old_row+i*MOVEMENT_SIZE, self.old_col])
                    pygame.display.update()
            else:
                for i in range(TILE_SIZE/MOVEMENT_SIZE):
                    self.draw_screen_layers()
                    self.screen.blit(self.__getattribute__(blit), [self.old_row-i*MOVEMENT_SIZE, self.old_col])
                    pygame.display.update()

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
