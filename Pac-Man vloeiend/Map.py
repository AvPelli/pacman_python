from copy import deepcopy

import pygame as pg  # Importeren van pg module
from Candy import Candy
from Coordinate import Coordinate


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
        self.__init_items()

    """Draw methods"""

    # Draws the map based on the signs in the Map dictionary
    def draw_map(self):
        for row in range(0, self.__tiles_vert_size):
            for col in range(0, self.__tiles_horiz_size):  # = Amount of tiles in 1 row
                tile_sign = self.__map[row][col]
                self.__game_display.blit(self.__tiles[tile_sign], (col * self.__tile_size, row * self.__tile_size))

    # Method for drawing a grid over the map, handy for debugging ect
    def draw_grid(self):
        """ Draws a grid to mark the tile borders """
        # (200, 10, 20): is kleur rood
        # pg.draw.line(self.gameDisplay, (200, 10, 20), (0, self.tile_size), (self.__width, self.tile_size))
        for x in range(0, self.__tiles_horiz_size):
            pg.draw.line(self.__game_display, (169, 169, 169), (self.__tile_size * x, 0),
                         (self.__tile_size * x, self.__height))
        for y in range(0, self.__tiles_vert_size):
            pg.draw.line(self.__game_display, (169, 169, 169), (0, self.__tile_size * y),
                         (self.__width, self.__tile_size * y))

    # This method redraws some items like:
    # All the remaining candy and the map itself
    def redraw_everything(self):
        self.draw_map()
        for candy in self.__candy_dict.values():
            candy.draw(candy.getCoord())

    """Initialize methods"""

    # Initialize all the items:
    # *   Makes a dictionary {Coordinate : Candy}
    # *   Initialise PacMan start coordinate
    # *   Makes a list of coordinates where there are walls
    def __init_items(self):
        for y in range(3, self.__tiles_vert_size):
            for x in range(0, self.__tiles_horiz_size):
                if self.__map[y][x] == "f":  # Place where candy show be drawn
                    coord = Coordinate(x - 1, y - 4)
                    self.__candy_dict[coord] = (Candy(self.__game_display, coord))
                elif self.__map[y][x] == "P":  # Place where PacMan needs to be located
                    self.__pacman_coord = Coordinate(x - 1, y - 4)
                elif self.__map[y][x] in "/=.-_\éè\()}{][abcd12345678uijo":  # All the characters that are walls
                    self.__wall_list.append(Coordinate(x - 1, y - 4))

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
        return deepcopy(self.__pacman_coord)

    # Getter: returns a copy of the list of walls (coordinates inside of the list)
    def get_wall_list(self):
        return deepcopy(self.__wall_list)

    # Getter: returns a the game_display
    def get_game_display(self):
        return self.__game_display

    # Getter: returns the dictionary, Coordinates mapped on a Candy Object
    def get_candy_dict(self):
        return self.__candy_dict
