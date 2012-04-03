import pygame

from constants import *

class GameScreen(object):
    
    def __init__(self):
        ''' Does the initial drawing of the game screen.
        '''
        self.screen = pygame.display.set_mode((1280, 832))
        self.font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 20)
        self.bg = pygame.image.load(IMG_DIR + 'rainbowbg.png')
        self.player_blit = pygame.image.load(IMG_DIR + 'dude.png')
        self.screen.blit(self.bg, (0,0))
        self.inventory_screen = self.small_font.render("Inventory", True, WHITE, BLACK)
        self.draw_alert("Welcome to Katie's Roguelike!")
        self.stats_screen = self.small_font.render("ARGH", True, WHITE, BLACK)
        pygame.display.flip()

    def draw_player(self, coord):
        ''' Draws the player at a specific coordinate
        '''
        self.screen.blit(self.player_blit, coord)

    def draw_stats(self, player_stats, color=WHITE):
        ''' Renders the stats for the player
        '''
        self.screen.blit(self.stats_screen, (1008, 0))
        self.stats_screen = self.small_font.render(player_stats.name, True, color, BLACK)
        self.screen.blit(self.stats_screen, (1008, 0))
        self.stats_screen = self.small_font.render("Level: " + str(player_stats.level), True, color, BLACK)
        self.screen.blit(self.stats_screen, (1008, 15))
        self.stats_screen = self.small_font.render("HP: %s/%s" % (str(player_stats.current_hp), str(player_stats.max_hp)), True, color, BLACK)
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
        self.screen.blit(self.alert, (0, 790))
        pygame.display.flip()

    def draw_inventory(self, inventory):
        ''' Renders the inventory for the user
        '''
        self.screen.blit(self.inventory_screen, (1008, 100))
        items = inventory.get_items()
        for i in range(items.__len__()):
            line = self.small_font.render(LONG_STRING, True, BLACK, BLACK)
            self.screen.blit(line, (1008, ((i+1)*15)+100))
        pygame.display.flip()
        for item in items:
            line = self.small_font.render(item, True, WHITE, BLACK)
            self.screen.blit(line, (1008, (items.index(item)+1)*15+100))

    def draw_treasure(self, treasure_map):
        ''' Draws the treasure chests yet to be opened.
        '''
        for row in range(ROWS):
            for col in range(COLUMNS):
                if treasure_map[row][col] != 0:
                    treasure = pygame.image.load(IMG_DIR + 'chest.png')
                    self.screen.blit(treasure, (row*TILE_SIZE, col*TILE_SIZE))
    
    def draw_monsters(self, map):
        ''' Draws monsters that appear in the area that the rogue can see
        '''
        for row in range(ROWS):
            for col in range(COLUMNS):
                if map.monsters[row][col] != 0 and map.current[row][col] != 0:
                    monster = pygame.image.load(IMG_DIR + 'dumb_monster.png')
                    self.screen.blit(monster, (row*TILE_SIZE, col*TILE_SIZE))
    
    def draw_walls(self, walls):
        ''' Draws walls on the game map
        '''
        for row in range(ROWS):
            for col in range(COLUMNS):
                if walls[row][col] != 0:
                    wall = pygame.image.load(IMG_DIR + 'wall.png')
                    self.screen.blit(wall, (row*TILE_SIZE, col*TILE_SIZE))

    def draw_darkness(self, map):
        ''' Draws the darkness and shadows on the board. 0 is dark, 1 is in shadows,
        '''
        for row in range(ROWS):
            for col in range(COLUMNS):
                if map.cleared[row][col] == 0:
                    if not map.current[row][col]:
                        pygame.draw.rect(self.screen, BLACK, (row*TILE_SIZE, col*TILE_SIZE, TILE_SIZE, TILE_SIZE))  
                if map.cleared[row][col] == 1:
                    if not map.current[row][col]:
                        shadow = pygame.Surface((TILE_SIZE, TILE_SIZE))
                        shadow.set_alpha(200)
                        shadow.fill(BLACK)
                        self.screen.blit(shadow, (row*TILE_SIZE, col*TILE_SIZE))

    def draw_background(self):
        ''' Draws my glorious background.
        '''
        self.screen.blit(self.bg, (0,0))

    def draw_screen_layers(self, map, player_stats):
        ''' Draws the layers of the game screen
        '''
        self.draw_background()
        #self.draw_treasure(map.treasure)
        self.draw_walls(map.walls)
        #self.draw_monsters(map)
        #self.draw_darkness(map)
        #self.draw_stats(player_stats=player_stats)
        #self.draw_player(coord=map.player)
        pygame.display.flip()

    def animate_move(self, hor, vert, blit):
        ''' This function is NOT USED. In theory, it animates a blit, but it makes everything look awful.
        '''
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