import pygame  # Importeren van pygame module
import sys
import importlib
from Map import *

pygame.init()  # Init of pygame

width = 224 * 2
height = 288 * 2
resolution = (width, height)

gameDisplay = pygame.display.set_mode(resolution)
pygame.display.set_caption('Pac-Man');
clock = pygame.time.Clock()


class Game():

    def __init__(self):
        gameDisplay.fill((0, 0, 0))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # print(event)
            map = Map(gameDisplay)
            map.draw_grid()
            pygame.display.update()

        pygame.quit()
        sys.exit()


game = Game()
game.run()

