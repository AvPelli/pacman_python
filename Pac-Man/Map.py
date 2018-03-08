import pygame  # Importeren van pygame module
import sys
import importlib
from Map import *

pygame.init()


class Map():

    def __init__(self, gameDisplay, width, height, tile_size):
        # Deze twee zullen altijd constant blijven
        self.tiles_vert_size = 28
        self.tiles_horiz_size = 36

        # Resolutie die wordt meegegeven niet, moet later nog eventueel aanpasbaar zijn?
        self.gameDisplay = gameDisplay  # The display of the game
        self.width = width
        self.height = height
        self.tile_size = tile_size

        # Map and tile info
        self.map = []
        # Dictionarie met elk getal komt een bepaalde tegel overeen (ordelijker dan cases)
        tile_black = pygame.image.load('tile_black.png')
        self.tiles = {1: tile_black}

        filename = "black.txt"
        with open(filename) as f:
            for line in f.readlines():
                self.map.append(line.strip().split(" "))

    def draw_grid(self):
        # Overzichtelijk om te zien waar de tiles zich bevinden.
        # (200, 10, 20): is kleur rood
        # pygame.draw.line(self.gameDisplay, (200, 10, 20), (0, self.tile_size), (self.width, self.tile_size))
        pygame.display.update()
        for x in range(0, self.tiles_vert_size):
            pygame.draw.line(self.gameDisplay, (200, 10, 20), (self.tile_size * x, 0),
                             (self.tile_size * x, self.height))
        for y in range(0, self.tiles_horiz_size):
            pygame.draw.line(self.gameDisplay, (200, 10, 20), (0, self.tile_size * y), (self.width, self.tile_size * y))

    def draw_map(self):
        for x in range(0, self.tiles_vert_size):
            for y in range(0, self.tiles_horiz_size):
                # self.gameDisplay.blit(self.tiles[1], (0, 0))
                self.gameDisplay.blit(self.tiles[1], (x*self.tile_size, y*self.tile_size))

