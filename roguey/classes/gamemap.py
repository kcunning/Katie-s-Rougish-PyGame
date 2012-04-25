# INTIALISATION
import pygame, math, sys, random, pickle
from pygame.locals import *
from random import randint, choice
import xml.etree.ElementTree as etree

from constants import *
from items import Treasure
from monsters import Derpy

class Map(object):
    ''' Stores the values for the map, but doesn't render it for the game. 

        Map.cleared = The cleared squares
    '''
    def __init__(self):
        ''' Sets all squares to uncleared.
        '''
        self.cleared = self.get_blank_map()
        self.current = self.get_blank_map()
        self.treasure = self.get_blank_map()
        self.walls = self.get_blank_map()
        self.monsters = self.get_blank_map()
        self.player = (0,0)
        self.floor = self.get_blank_map() 
        self.roomlist = []

        self.get_rooms()
        self.connect_rooms()

        all_treasures = self.get_all_treasures()
        for i in range(TREASURES):
            while 1:
                col = random.randint(0, COLUMNS-1)
                row = random.randint(0, ROWS-1)
                if not self.treasure[row][col] and self.floor[row][col]:
                    self.treasure[row][col] = choice(all_treasures)
                    break

        for i in range(MONSTERS):
            while 1:
                col = random.randint(0, COLUMNS-1)
                row = random.randint(0, COLUMNS-1)
                if not self.treasure[row][col] and self.floor[row][col]:
                    self.monsters[row][col] = Derpy()
                    break
        self.fill_map()

    def get_all_treasures(self):
        f = open("roguey/resources/items.xml")
        root = etree.fromstring(f.read())
        treasures = [Treasure.from_xml(t) for t in root]
        f.close()
        return treasures

    def fill_map(self):
        for i in range(ROWS):
            for j in range(COLUMNS):
                    if not self.floor[i][j]:
                        self.walls[i][j] = 1

    def get_rooms(self):
        # Set initial room
        room = self.check_room(coord=(0,0), height=5, length=5)
        self.roomlist.append(room)
        rooms = 1
        keep_going = 50
        while rooms <= MAX_ROOMS and keep_going:
            height = randint(4,10)
            length = randint(4,10)
            x = randint(0, COLUMNS-1)
            y = randint(0, ROWS)
            room = self.check_room(coord=(x,y), height=height, length=length)
            if room:
                rooms += 1
                self.roomlist.append(room)
            else:
                keep_going -=1
        for room in self.roomlist:
            self.make_random_door(room)

    def connect_rooms(self):
        for room in self.roomlist:
            i = self.roomlist.index(room)
            try:
                next = self.roomlist[i+1]
            except:
                next = self.roomlist[0]
            if room.door[0] < next.door[0]:
                start = room.door[0]
                end = next.door[0]
            else:
                start = next.door[0]
                end = room.door[0]
            for x in range(start, end):
                self.walls[x][room.door[1]] = 0
                self.floor[x][room.door[1]] = 1
            if room.door[1] < next.door[1]:
                start = room.door[1]
                end = next.door[1]
            else:
                start = next.door[1]
                end = room.door[1]
            for y in range(start, end):
                self.walls[next.door[0]][y] = 0
                self.floor[next.door[0]][y] = 1

    def check_room(self, coord, height, length):
        ''' Are all the spaces in a room free?
        '''
        for i in range(0, height):
            for j in range(0, length):
                if coord[1] + i > COLUMNS-1:
                    return False
                if coord[0] + j > ROWS-1:
                    return False
                if self.floor[coord[0]+j][coord[1]+i]:
                    return False
        room = Room(start=coord, height=height, width=length)
        self.create_room(room)
        return room

    def make_random_door(self, room):
        while True:
            wall = choice(DIRECTIONS)
            if wall in ['north', 'south']:
                block = randint(1, room.width-2)
            else:
                block = randint(1, room.height-2)
            if wall == 'north':
                coord = (room.start[0]+block,room.start[1])
                check = (coord[0], coord[1]-1)
                next = (coord[0], coord[1]-2)
            if wall == 'south':
                coord = (room.start[0]+block, room.start[1]+room.height-1)
                check = (coord[0], coord[1]+1)
                next = (coord[0], coord[1]+1)
            if wall == 'east':
                coord = (room.start[0],room.start[1]+block)
                check = (coord[0]-1, coord[1])
                next = (coord[0]-2, coord[1])
            if wall == 'west':
                coord = (room.start[0]+room.width-1, room.start[1]+block)
                check = (coord[0]+1, coord[1])
                next = (coord[0]+2, coord[1])
            door = self.check_door(coord, check, next)
            if door:
                self.walls[coord[0]][coord[1]] = 0
                self.floor[coord[0]][coord[1]] = 2
                room.door = (coord[0],coord[1])
                return

    def check_door(self, coord, check, next):
        # Is it at the bounds?
        if check[0] < 0 or check[1] < 0:
            return False
        # Is it next to a wall?
        try:
            if self.walls[check[0]][check[1]]:
                # Is that wall next to another wall?
                if self.walls[next[0]][next[1]]:
                    return False
                else:
                    try:
                        self.walls[check[0]][check[1]] = 0
                    except:
                        pass # Sometimes, we're one away from the border. That's okay.
        except:
            return False
        return True


    def create_room(self, room):
        # make top and bottom walls
        for i in range(0, room.width):
            self.walls[room.start[0]+i][room.start[1]] = 1
            self.walls[room.start[0]+i][room.start[1]+room.height-1] = 1
        # make side walls
        for i in range(0, room.height):
            self.walls[room.start[0]][room.start[1]+i] = 1
            self.walls[room.start[0]+room.width-1][room.start[1]+i] = 1
        # fill in the floor
        for x in range (1, room.width-1):
            for y in range (1, room.height-1):
                self.floor[room.start[0]+x][room.start[1]+y] = 1

        

    def get_blank_map(self):
        ''' Returns a map with all values set to 0
        '''
        map = []
        for i in range(ROWS):
                        row = []
                        for j in range(COLUMNS):
                                row.append(0)
                        map.append(row)
        return map
    
    def is_block_empty(self, row, col):
        if not self.treasure[row][col] and not self.monsters[row][col] and not self.walls[row][col]\
        and not (self.player[0]/TILE_SIZE, self.player[1]/TILE_SIZE) == (row, col):
            return True
        else:
            return False

    def has_wall(self, row, col):
        row = row/TILE_SIZE
        col = col/TILE_SIZE
        if self.walls[row][col]:
            return True
        else:
            return False

    def has_monster(self, row, col):
        row = row/TILE_SIZE
        col = col/TILE_SIZE
        if self.monsters[row][col]:
            return True
        else:
            return False
    
    def set_current_position(self, position):
        self.current = self.get_blank_map()
        row, col = position
        row = row/TILE_SIZE
        col = col/TILE_SIZE
        self.current[row][col] = 1
        for i in range(RADIUS):
            if row-i > 0:
                self.current[row-i-1][col] = 1
            if row+i < ROWS-1:
                self.current[row+i+1][col] = 1
            if col-i > 0:
                self.current[row][col-i-1] = 1
            if col+i < COLUMNS-1:
                self.current[row][col+i+1] = 1
        for i in range(RADIUS-1):
            if row-i > 0 and col-i > 0: self.current[row-i-1][col-i-1] = 1
            if row-i > 0 and col-i < COLUMNS-1: self.current[row-i-1][col+i+1] = 1
            if row+i < ROWS-1 and col-i > 0: self.current[row+i+1][col-i-1] = 1
            if row+i < ROWS-1 and col+i < COLUMNS-1: self.current[row+i+1][col+i+1] = 1

    def clear_block(self, position):
        ''' Given the current position of the player, sets the current square to completely cleared, 
                and the squares nearby to partially cleared.
        '''
        x, y = position
        col = y/TILE_SIZE
        row = x/TILE_SIZE
        
        self.cleared[row][col] = 1
        if row < ROWS-1:
            self.cleared[row+1][col] = 1
        if row > 0:
            self.cleared[row-1][col] = 1
        if col < COLUMNS-1:
            self.cleared[row][col+1] = 1
        if col > 0:
            self.cleared[row][col-1] = 1
    
    def get_all_monsters(self):
        monsters = {}
        for row in range(ROWS):
            for col in range(COLUMNS):
                if self.monsters[row][col]:
                    monsters[self.monsters[row][col]] = [row, col]
        return monsters

    def clear_treasure(self, position):
        ''' Given a position, clears the treasure from it, and returns the treasure.
        ''' 
        x, y = position
        row = x/TILE_SIZE
        col = y/TILE_SIZE
        treasure = self.treasure[row][col]
        self.treasure[row][col] = 0
        return treasure

    def print_ascii_map(self):
        ''' Prints an ascii map to the console. For troubleshooting only.
        '''
        for row in self.floor:
            print row, row.__len__()

    def move_monsters(self):
        monsters = self.get_all_monsters()
        for monster in monsters.keys():
            if monster.current_hp <= 0:
                r, c = monsters[monster]
                self.monsters[r][c] = 0
            else:
                d = random.sample(DIRECTIONS, 1)[0]
                new_row, new_col = row, col = monsters[monster]
                if d == "north":
                    new_row -= 1
                if d == "south":
                    new_row += 1
                if d == "east":
                    new_col += 1
                if d == "west":
                    new_col -= 1
                try:
                    if self.is_block_empty(new_row, new_col) and new_row > 0 and new_col > 0:
                        self.monsters[new_row][new_col] = monster
                        self.monsters[row][col] = 0
                except:
                    pass # Monsters can run into walls, edges, chests, etc. It consumes their turn.

class Room(object):

    def __init__(self, height=5, width=5, start=(0,0)):
        self.title = "Generic room"
        self.start = start
        self.width = width
        self.height = height
        self.end = (self.start[0]+self.width, self.start[1]+self.width)
        self.door = []