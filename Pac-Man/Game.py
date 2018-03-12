import pygame  # Importeren van pygame module
import sys
import importlib
from Map import *

pygame.init()  # Init of pygame

width = 224 * 3
height = 288 * 3
tile_size = 8*3
resolution = (width, height)

gameDisplay = pygame.display.set_mode(resolution)
pygame.display.set_caption('Pac-Man');
clock = pygame.time.Clock()

#Test

class Game():

    def __init__(self):
        gameDisplay.fill((255, 255, 255))
        self.map = Map(gameDisplay, width, height, tile_size)
        self.map.draw_map()
        self.map.draw_grid()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # print(event)

            pygame.display.update()

        pygame.quit()
        sys.exit()


game = Game()
game.run()

