from copy import deepcopy

import pygame as pg  # Importeren van pg module

from Candy import Candy
from Coordinate import Coordinate
from Gate import Gate
from SuperCandy import SuperCandy


class Map():

    # Constructor of Map

    def __init__(self, game_display, width, height, tile_size):
        # Amount of rows en colums
        self.__tiles_horiz_size = 28
        self.__tiles_vert_size = 36

        # Screen and Resolution variables
        self.__game_display = game_display  # The display of the game
        self.__width = width
        self.__height = height
        self.__tile_size = tile_size

        # Makes dictionary, maps  a Character on an specific image
        self.__tiles = {}
        self.__init_tiles()

        # Makes the tilemap
        filename = "res/files/maze2.txt"
        self.__map = [line.split() for line in open(filename, 'r')]

        # Item lists/ditcionaries
        self.__wall_list = list()
        self.__candy_dict = {}
        self.__ghosts_coord = list()
        self.__init_items()
        self.__transp_list = list()

        # Pacman himself
        self.__pacman = None

        # Font settings
        self.font_obj = pg.font.Font("res/files/fonts/emulogic.ttf", 16)
        self.oneup = True
        self.fontoffset = 3

        # Map settings
        self.clock = pg.time.Clock()
        self.upcounter = 0

    def draw_map(self):
        for row in range(0, self.__tiles_vert_size):
            for col in range(0, self.__tiles_horiz_size):  # = Amount of tiles in 1 row
                tile_sign = self.__map[row][col]
                self.__game_display.blit(self.__tiles[tile_sign], (col * self.__tile_size, row * self.__tile_size))
        self.draw_extra()

    def draw_extra(self):
        self.draw_lifes()
        self.draw_text("HIGHSCORE",9,0,(0,255,0))
        self.draw_grid()
        self.draw_score()

    # Method for drawing the amount of lives pacman has left
    def draw_lifes(self):
        width = self.__tile_size * 2
        height = self.__tile_size * (self.__tiles_vert_size - 2)
        lifesimg = pg.image.load("res/tileset/pacman_lifes.png")
        img_width = lifesimg.get_width()
        for i in range(0, self.__pacman.get_lifes()):
            self.__game_display.blit(lifesimg, (width, height))
            width += img_width

    # Draw text with a given coordinate and color(as a tuple). x en y depends on the tile_size
    def draw_text(self,text,x,y,color_rgb=(255,255,255)):
        text_surface_obj = self.font_obj.render(text, False, color_rgb)
        self.__game_display.blit(text_surface_obj, (x * self.__tile_size, y * self.__tile_size - self.fontoffset))

    def draw_oneup(self):
        duration = 60
        if self.upcounter < duration:
            self.oneup = False
            self.draw_text('1UP',3,0,(255,0,0))
            self.upcounter += 1
        elif self.upcounter >= duration and self.upcounter < duration * 2:
            self.oneup = True
            self.draw_text('',3,0)
            self.upcounter += 1
            if self.upcounter == duration * 2:
                self.upcounter = 0

    # Method for drawing the score
    def draw_score(self):
        score = self.__pacman.get_score()
        scorestr = str(self.__pacman.get_score())
        if score < 10:
            scorestr = str(0) + scorestr
        score_size = len(scorestr)
        text_surface_obj = self.font_obj.render(scorestr, False, (255, 255, 255))
        self.__game_display.blit(text_surface_obj,
                                 (7 * self.__tile_size - score_size * 16, self.__tile_size - self.fontoffset))

    # Method for drawing a grid over the map, handy for debugging ect
    def draw_grid(self):
        """ Draws a grid to mark the tile borders """
        # (200, 10, 20): is kleur rood
        # pg.draw.line(self.gameDisplay, (200, 10, 20), (0, self.__tile_size), (self.__width, self.__tile_size))
        for x in range(0, self.__tiles_horiz_size):
            pg.draw.line(self.__game_display, (169, 169, 169), (self.__tile_size * x, 0),
                         (self.__tile_size * x, self.__height))
        for y in range(0, self.__tiles_vert_size):
            pg.draw.line(self.__game_display, (169, 169, 169), (0, self.__tile_size * y),
                         (self.__width, self.__tile_size * y))

    # Draws start Pacman
    def draw_startpacman(self, coordinate):
        self.__pacman.draw_startpacman(coordinate)

    # Draws Pacman his death animation
    def draw_pacmandeathani(self, deadco):
        imagefolder = "res/pacmandeath/"
        for x in range(1, 12):
            pg.time.delay(100)
            self.draw_map()
            self.draw_candy()
            self.draw_oneup()
            pacmanimgdeath = pg.image.load(imagefolder + str(x) + ".png")
            self.__game_display.blit(pacmanimgdeath, deadco.get_pixel_tuple())

            pg.display.update()

    # This method redraws some items like:
    # All the remaining candy and the map itself
    def draw_candy(self):
        self.draw_map()
        for candy in self.__candy_dict.values():
            candy.draw(candy.get_coord())
    #This method will change the color of the walls
    def change_wall_color(self,won=True):
        filename = "res/files/tile_codering.txt"
        for line in open(filename, 'r'):
            sign_tilename = line.strip().split(" : ")
            if(won):
                 tile_name = "res/tileset/Game-won/" + sign_tilename[1] + ".png"
            else:
                 tile_name = "res/tileset/" + sign_tilename[1] + ".png"

            self.__tiles[sign_tilename[0]] = pg.image.load(tile_name)

    """Initialize methods"""

    # Initialize all the items:
    # *   Makes a dictionary {Coordinate : Candy}
    # *   Initialise PacMan start coordinate
    # *   Makes a list of coordinates where there are walls
    def __init_items(self):
        map_noborders = self.__map[3:]
        self.__gates_dict = {}
        self.gate_list = list()
        for y in range(0, len(map_noborders)):
            for x in range(0, len(map_noborders[0])):
                if map_noborders[y][x] == "f":  # Place where candy show be drawn
                    coord = Coordinate(x, y)
                    self.__candy_dict[coord] = (Candy(self.__game_display, coord))
                elif map_noborders[y][x] == "D":
                    coord = Coordinate(x, y)
                    self.__candy_dict[coord] = (SuperCandy(self.__game_display, coord))
                elif map_noborders[y][x] == "P":  # Place where PacMan needs to be located
                    self.__pacman_coord = Coordinate(x, y)
                elif map_noborders[y][x] in "/=.-_\éè\()}{][abcd12345678uijonq":  # All the characters that are walls
                    self.__wall_list.append(Coordinate(x, y))
                elif map_noborders[y][x] == 'g':
                    self.__ghosts_coord.append(Coordinate(x, y))
                elif "t" in map_noborders[y][x]:
                    # At a teleporter, add some "fake" walls to the list to make sure pacman doesn't go out of bounds
                    self.add_gate(map_noborders[y][x], Coordinate(x, y))
                    self.__wall_list.append(Coordinate(x - 1, y - 1))
                    self.__wall_list.append(Coordinate(x - 1, y + 1))
                    self.__wall_list.append(Coordinate(x + 1, y - 1))
                    self.__wall_list.append(Coordinate(x + 1, y + 1))
        self.make_gate_list()

    # Initialization of a dictionary, every sign is equivalent to a tile image
    def __init_tiles(self):
        filename = "res/files/tile_codering.txt"
        for line in open(filename, 'r'):
            sign_tilename = line.strip().split(" : ")
            tile_name = "res/tileset/" + sign_tilename[1] + ".png"
            self.__tiles[sign_tilename[0]] = pg.image.load(tile_name)

    """Getters"""

    # Getter: returns a copy of pacman his start coordinate
    def get_pacman_start(self):
        return self.__pacman_coord

    def get_ghosts_start(self):
        return self.__ghosts_coord

    # Getter: returns a copy of the list of walls (coordinates inside of the list)
    def get_wall_list(self):
        return deepcopy(self.__wall_list)

    # Getter: returns the dictionary, Coordinates mapped on a Candy Object
    def get_candy_dict(self):
        return self.__candy_dict

    # Getter: returns list of transporters
    def get_transporters(self):
        return self.__transp_list

    def get_gates(self):
        return self.gate_list

    def get_tiles_horiz_size(self):
        return self.__tiles_horiz_size

    def get_tiles_vert_size(self):
        return self.__tiles_vert_size

    """Setters"""

    # Setter: sets the pacman object

    def set_pacman(self, p):
        self.__pacman = p

    def add_gate(self, gate_number, coordinate):
        if len(self.__gates_dict.keys()) == 0 or gate_number not in self.__gates_dict.keys():
            self.__gates_dict[gate_number] = list()
        self.__gates_dict[gate_number].append(coordinate)

    def make_gate_list(self):
        for gate_number in self.__gates_dict:
            self.gate_list.append(Gate(self.__gates_dict[gate_number][0], self.__gates_dict[gate_number][1]))
