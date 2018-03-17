import pygame  # Importeren van pygame module
import sys
import importlib
from Map import *

pygame.init()


class Map():

    def __init__(self, game_display, width, height, tile_size):
        # Deze twee zullen altijd constant blijven
        self.tiles_horiz_size = 28
        self.tiles_vert_size = 36

        # Resolutie die wordt meegegeven niet, moet later nog eventueel aanpasbaar zijn?
        self.game_display = game_display  # The display of the game
        self.width = width
        self.height = height
        self.tile_size = tile_size

        # Map and tile info
        self.map = []
        # Aanmaken dictionarie met elk getal komt een bepaalde tegel overeen (ordelijker dan cases)
        self.tiles = {}
        self.init_tiles()

        # Aanmaken tilemap
        filename = "maze2.txt"
        self.map = [line.split() for line in open(filename, 'r')]

    def draw_grid(self):
        """ Draws a grid to mark the tile borders """
        # Overzichtelijk om te zien waar de tiles zich bevinden.
        # (200, 10, 20): is kleur rood
        # pygame.draw.line(self.gameDisplay, (200, 10, 20), (0, self.tile_size), (self.width, self.tile_size))

        pygame.display.update()
        for x in range(0, self.tiles_horiz_size):
            pygame.draw.line(self.game_display, (169, 169, 169), (self.tile_size * x, 0),
                             (self.tile_size * x, self.height))
        for y in range(0, self.tiles_vert_size):
            pygame.draw.line(self.game_display, (169, 169, 169), (0, self.tile_size * y),
                             (self.width, self.tile_size * y))

    def draw_map(self):
        """ Draws the map based on the signs in the Map dictionary """
        print(str(self.tiles_horiz_size - 1), " " + str(self.tiles_vert_size - 1))
        for row in range(0, self.tiles_vert_size):
            for col in range(0, self.tiles_horiz_size):  # = Amount of tiles in 1 row
                tile_sign = self.map[row][col]
                self.game_display.blit(self.tiles[tile_sign], (col * self.tile_size, row * self.tile_size))

    def init_tiles(self):
        """ Initialization of a dictionary, every sign is equivalent to a tile image """
        filename = "tile_codering.txt"
        for line in open(filename, 'r'):
            sign_tilename = line.strip().split(" : ")
            tile_name = "Tileset/" + sign_tilename[1] + ".png"
            self.tiles[sign_tilename[0]] = pygame.image.load(tile_name)
