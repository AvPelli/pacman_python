import pygame  # Importeren van pygame module
from Map import *

#SLECHTE KLASSE ---> GOED IS IN TEST PACKAGE!!
class Pacman:
    def __init__(self, screen, direction, x, y):
        self.pacmanPic = pygame.image.load('pacmanOpen.png')
        self.screen = screen
        self.screen.blit(self.pacmanPic, (x, y))
        self.direction = "RIGHT"
        self.x = x
        self.y = y
        self.dict = {"RIGHT": (50, 0)}
        self.screenPixelPos = (0, 0)

    def move(self):
        (addX, addY) = self.dict[self.direction]
        self.screen.blit(self.pacmanPic,
                         (self.x + addX - self.screenPixelPos[0], self.y + addY - self.screenPixelPos[1]))
        self.x, self.y = self.x + addX, self.y + addY
