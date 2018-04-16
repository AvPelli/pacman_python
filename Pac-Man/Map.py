from copy import deepcopy

import pygame as pg  # Importeren van pg module

from Candy import Candy
from Coordinate import Coordinate


class Map():

    # Constructor of Map

    def __init__(self, game_display, width, height, tile_size):
        # Amount of rows en colums
        self.tiles_horiz_size = 28
        self.tiles_vert_size = 36

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

        # Gate dicitionary
        self.gates_dict = {}

        # Pacman himself
        self.pacman = None

        # Font settings
        self.font_obj = pg.font.Font("res/files/fonts/emulogic.ttf", 16)
        self.oneup = True
        self.fontoffset = 3

        # Map settings
        self.upcounter = 0

    def draw_map(self):
        for row in range(0, self.tiles_vert_size):
            for col in range(0, self.tiles_horiz_size):  # = Amount of tiles in 1 row
                tile_sign = self.__map[row][col]
                self.__game_display.blit(self.__tiles[tile_sign], (col * self.__tile_size, row * self.__tile_size))
        self.draw_extra()

    def draw_extra(self):
        self.draw_lifes()
        self.draw_hsletters()
        self.draw_grid()
        self.draw_score()

    # Method for drawing the amount of lives pacman has left
    def draw_lifes(self):
        width = self.__tile_size * 2
        height = self.__tile_size * (self.tiles_vert_size - 2)
        lifesimg = pg.image.load("res/tileset/pacman_lifes.png")
        img_width = lifesimg.get_width()
        for i in range(0, self.pacman.getLifes()):
            self.__game_display.blit(lifesimg, (width, height))
            width += img_width

    # Method for drawing the high score letters
    def draw_hsletters(self):
        text_surface_obj = self.font_obj.render('HIGH SCORE', False, (255, 255, 255))
        self.__game_display.blit(text_surface_obj, (9 * self.__tile_size, 0 - self.fontoffset))

    # Draw Ready! text, displayed at the start of the game
    def draw_readytext(self):
        text_surface_obj = self.font_obj.render('READY!', False, (255, 238, 0))
        self.__game_display.blit(text_surface_obj, (11 * self.__tile_size, 20 * self.__tile_size - self.fontoffset))

    def remove_readytext(self):
        text_surface_obj = self.font_obj.render('      ', False, (0, 0, 0))
        self.__game_display.blit(text_surface_obj, (11 * self.__tile_size, 20 * self.__tile_size - self.fontoffset))

    def draw_oneup(self):
        duration = 60
        if self.upcounter < duration:
            self.oneup = False
            text_surface_obj = self.font_obj.render('1UP', False, (255, 255, 255))
            self.upcounter += 1
            self.__game_display.blit(text_surface_obj, (3 * self.__tile_size, -self.fontoffset))
        elif self.upcounter >= duration and self.upcounter < duration * 2:
            self.oneup = True
            text_surface_obj = self.font_obj.render('      ', False, (255, 255, 255))
            self.upcounter += 1
            if self.upcounter == duration * 2:
                self.upcounter = 0
            self.__game_display.blit(text_surface_obj, (3 * self.__tile_size, -self.fontoffset))

    # Method for drawing the score
    def draw_score(self):
        score = self.pacman.getScore()
        scorestr = str(self.pacman.getScore())
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
        # pg.draw.line(self.gameDisplay, (200, 10, 20), (0, self.tile_size), (self.__width, self.tile_size))
        for x in range(0, self.tiles_horiz_size):
            pg.draw.line(self.__game_display, (169, 169, 169), (self.__tile_size * x, 0),
                         (self.__tile_size * x, self.__height))
        for y in range(0, self.tiles_vert_size):
            pg.draw.line(self.__game_display, (169, 169, 169), (0, self.__tile_size * y),
                         (self.__width, self.__tile_size * y))

    # Draws start Pacman
    def draw_startpacman(self):
        self.pacman.draw_startpacman()

    # This method redraws some items like:
    # All the remaining candy and the map itself
    def draw_candy(self):
        self.draw_map()
        for candy in self.__candy_dict.values():
            candy.draw(candy.get_coord())

    """Initialize methods"""

    # Initialize all the items:
    # *   Makes a dictionary {Coordinate : Candy}
    # *   Initialise PacMan start coordinate
    # *   Makes a list of coordinates where there are walls
    def __init_items(self):
        map_noborders = self.__map[3:]
        for y in range(0, len(map_noborders)):
            for x in range(0, len(map_noborders[0])):

                if map_noborders[y][x] == "f":  # Place where candy show be drawn
                    coord = Coordinate(x, y)
                    self.__candy_dict[coord] = (Candy(self.__game_display, coord))
                elif map_noborders[y][x] == "P":  # Place where PacMan needs to be located
                    self.__pacman_coord = Coordinate(x, y)
                elif map_noborders[y][x] in "/=.-_\éè\()}{][abcd12345678uijo":  # All the characters that are walls
                    self.__wall_list.append(Coordinate(x, y))
                elif map_noborders[y][x] == 'g':
                    self.__ghosts_coord.append(Coordinate(x, y))
                elif "t" in map_noborders[y][x]:
                    # At a teleporter, add some "fake" walls to the list to make sure pacman doesn't go out of bounds
                    self.__wall_list.append(Coordinate(x - 1, y - 1))
                    self.__wall_list.append(Coordinate(x - 1, y + 1))
                    self.__wall_list.append(Coordinate(x + 1, y - 1))
                    self.__wall_list.append(Coordinate(x + 1, y + 1))

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

    # Getter: returns a the game_display
    def get_game_display(self):
        return self.__game_display

    # Getter: returns the dictionary, Coordinates mapped on a Candy Object
    def get_candy_dict(self):
        return self.__candy_dict

    # Getter: returns list of transporters
    def get_transporters(self):
        return self.__transp_list

    """Setters"""

    # Setter: sets the pacman object
    def set_pacman(self, p):
        self.pacman = p
