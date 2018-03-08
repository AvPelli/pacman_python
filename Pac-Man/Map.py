import pygame  # Importeren van pygame module
import sys
import importlib
from Map import *

pygame.init()


class Map():
    def __init__(self, gameDisplay):
        self.gameDisplay = gameDisplay  # The display of the game

    def draw_grid(self):
        pygame.draw.line(self.gameDisplay, (200, 10, 20), (0, 8 * 2), (224 * 2, 8 * 2))
        pygame.display.update()
