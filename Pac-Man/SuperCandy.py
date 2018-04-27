import pygame as pg

from Character import Character
from Coordinate import Coordinate
from Direction import Direction
from Candy import Candy

class SuperCandy(Candy):
    def __init__(self, game_Display, coordinate):
        super().__init__(game_Display,coordinate)
        self._superimage = pg.image.load("res/candy/superdot.png")

    def draw(self, coordinate):
        (xPixels, yPixels) = (coordinate.get_pixel_tuple())
        self._game_Display.blit(self._superimage, (xPixels, yPixels))

    def get_score(self):
        return 100
