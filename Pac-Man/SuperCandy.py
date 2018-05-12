import pygame as pg

from Candy import Candy


class SuperCandy(Candy):
    def __init__(self, game_Display, coordinate):
        super().__init__(game_Display, coordinate)
        self._image = pg.image.load("res/candy/superdot.png")

    def get_score(self):
        return 100
