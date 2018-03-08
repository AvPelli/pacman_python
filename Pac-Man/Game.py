import pygame  # Importeren van pygame module
import sys
import importlib
from Map import*

pygame.init()  # Oproepen van de init() functie



width = 224*2
height = 288*2
resolution = (width, height)

gameDisplay = pygame.display.set_mode(resolution)
pygame.display.set_caption('Pac-Man');
clock = pygame.time.Clock()

class Game():
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False



                # print(event)
                pygame.display.update()

            gameDisplay.fill((0, 0, 0))
            pygame.draw.rect(gameDisplay, (200, 10, 20), pygame.Rect((100, 300), (20, 30)))
        pygame.quit()
        sys.exit()



game = Game()
game.run()
