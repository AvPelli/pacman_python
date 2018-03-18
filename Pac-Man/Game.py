import pygame  # Importeren van pygame module
import sys
import importlib
from Map import *

import pygame
from Map import Map
from Pacman import Pacman

pygame.mixer.pre_init(22050, 16, 2, 512)
pygame.mixer.init()

clock = pygame.time.Clock()
pygame.init()  # Init of pygame

width = 224 * 2
height = 288 * 2
tile_size = 8*2
resolution = (width, height)

game_display = pygame.display.set_mode(resolution)
pygame.display.set_caption('Pac-Man');
clock = pygame.time.Clock()
window = pygame.display.set_mode((1, 1))
pygame.display.set_caption('Pac-Man')
window = pygame.display.set_mode(resolution, pygame.DOUBLEBUF | pygame.HWSURFACE)
screen = pygame.display.get_surface()
gameDisplay = pygame.display.set_mode(resolution)


#Test

class Game():

    def __init__(self):
        game_display.fill((255, 255, 255))
        self.map = Map(game_display, width, height, tile_size)
        self.map.draw_map()
        self.map.draw_grid()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        print("LEFT")
                    elif event.key == pygame.K_RIGHT:
                        print("RIGHT")
                    elif event.key == pygame.K_UP:
                        print("UP")
                    elif event.key == pygame.K_DOWN:
                        print("DOWN")
            pygame.display.update()
            self.pacman.move()
            clock.tick(60)
        pygame.quit()
        sys.exit()


game = Game()
game.run()

