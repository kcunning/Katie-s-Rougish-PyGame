import pygame

from constants import *

class GameScreen(object):
    
    def __init__(self):
        ''' Does the initial drawing of the game screen.
        '''
        self.selected_tile = [0, 0]
        self.screen = pygame.display.set_mode((1280, 832))
        self.font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 20)
        self.bg = pygame.image.load(IMG_DIR + 'rainbowbg.png')
        self.player_blit = pygame.image.load(IMG_DIR + 'dude.png')
        self.monster_blit = pygame.image.load(IMG_DIR + 'dumb_monster.png')
        self.selection_blit = pygame.image.load(IMG_DIR + 'selection.png')
        self.treasure_blit = pygame.image.load(IMG_DIR + 'chest.png')
        self.wall_tile = pygame.image.load(IMG_DIR + 'wall.png')
        self.floor_tile = pygame.image.load(IMG_DIR + 'floor.png')
        self.screen.blit(self.bg, (0,0))
        self.inventory_screen = self.small_font.render("Inventory", True, WHITE, BLACK)
        self.equipment_screen = self.small_font.render("Equipment", True, WHITE, BLACK)
        self.draw_alert("Welcome to Katie's Roguelike!")
        self.stats_screen = self.small_font.render("ARGH", True, WHITE, BLACK)
        self.draw_inventory()
        self.draw_equipment()
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
        line = 30
        for stat in STATS:
            if hasattr(player_stats, stat):
                s = str(getattr(player_stats, stat))
            else:
                s = str(player_stats.stats[stat])
            self.stats_screen = self.small_font.render("%s: %s" % (stat, s), True, color, BLACK)
            self.screen.blit(self.stats_screen, (1008, line+15))
            line += 15
        self.stats_screen = self.small_font.render("Armor: %s" % player_stats.get_armor(), True, color, BLACK)
        self.screen.blit(self.stats_screen, (1008, line))
        line += 15

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

    def draw_equipment(self, equipment=START_EQUIPMENT):
        ''' Renders the equipment. Expect it to be exchanged for something
            awesomer
        ''' 
        self.screen.blit(self.equipment_screen, (1008, 200))
        for i in range(equipment.keys().__len__()):
            line = self.small_font.render(LONG_STRING, True, BLACK, BLACK)
            self.screen.blit(line, (1008, ((i+1)*15)+200))
        pygame.display.flip()
        i = 1
        for slot in EQUIPMENT_TYPES:
            try:
                line_text = slot + ":   " + equipment[slot].title
            except:
                line_text = slot + ":   "
            line = self.small_font.render(line_text, True, WHITE, BLACK)
            self.screen.blit(line, (1008, i*15+200))
            i += 1
        pygame.display.flip()

    def draw_inventory(self, inventory=None):
        ''' Renders the inventory for the user
        '''
        self.screen.blit(self.inventory_screen, (1008, 400))
        if inventory:
            items = inventory.get_items()
        else:
            items = []
        for i in range(items.__len__()):
            line = self.small_font.render(LONG_STRING, True, BLACK, BLACK)
            self.screen.blit(line, (1008, ((i+1)*15)+400))
        pygame.display.flip()
        for item in items:
            line = self.small_font.render(item.title, True, WHITE, BLACK)
            self.screen.blit(line, (1008, (items.index(item)+1)*15+400))

    def draw_treasure(self, treasure_map):
        ''' Draws the treasure chests yet to be opened.
        '''
        for row in range(ROWS):
            for col in range(COLUMNS):
                if treasure_map[row][col] != 0:
                    self.screen.blit(
                        self.treasure_blit,
                        (row*TILE_SIZE, col*TILE_SIZE))
    
    def draw_monsters(self, map):
        ''' Draws monsters that appear in the area that the rogue can see
        '''
        for row in range(ROWS):
            for col in range(COLUMNS):
                #if map.monsters[row][col] != 0 and map.current[row][col] != 0:
                if map.monsters[row][col] != 0:
                    self.screen.blit(
                        self.monster_blit,
                        (row*TILE_SIZE, col*TILE_SIZE))
    
    def draw_walls(self, walls, tile):
        ''' Draws walls on the game map
        '''
        for row in range(ROWS):
            for col in range(COLUMNS):
                if walls[row][col] != 0:
                    self.screen.blit(tile, (row*TILE_SIZE, col*TILE_SIZE))

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

    def draw_selection_square(self):
        '''Draw a selection square at the current mouse position
        '''
        mouse_pos = pygame.mouse.get_pos()
        self.selected_tile = [c / TILE_SIZE for c in mouse_pos]
        selection_pos = [c * TILE_SIZE for c in self.selected_tile]
        self.screen.blit(self.selection_blit, selection_pos)

    def draw_selected_square_info(self, map):
        '''Draw some info regarding the contents of the currently selected square'''
        x, y = self.selected_tile
        try:
            if map.monsters[x][y]:
                self.stats_screen = self.small_font.render(str(map.monsters[x][y]), True, (0, 255, 0, 255))
                self.screen.blit(self.stats_screen, (0, 0))
        except IndexError:
            # mouse probably off the map
            pass

    def draw_screen_layers(self, map, player_stats):
        ''' Draws the layers of the game screen
        '''
        self.draw_background()
        self.draw_walls(map.floor, self.floor_tile)
        self.draw_walls(map.walls, self.wall_tile)
        self.draw_treasure(map.treasure)
        self.draw_monsters(map)
        #self.draw_darkness(map)
        self.draw_stats(player_stats=player_stats)
        self.draw_player(coord=map.player)
        self.draw_selection_square()
        self.draw_selected_square_info(map)
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