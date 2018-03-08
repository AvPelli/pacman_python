import pygame  # Importeren van pygame module
import sys
import importlib
from Map import *

pygame.init()

class Map():
    def draw_grid(self):
        pygame.draw.line(pygame.display, "black", 250, 400)
