import pygame as pg
from Candy import Candy


class Fruit:
    def __init__(self, game_Display, coordinate, fruitselector, fruittype):
        self.__game_Display = game_Display
        self.__image = pg.image.load("res/fruit/" + fruittype + ".png")
        self.__coordinate = coordinate
        self.fruittype = fruittype
        self._fruitselector = fruitselector
        self.__bonus = self._fruitselector.get_fruitbonus(self.fruittype)
        print(self.__bonus)

    def draw(self):
        self.__game_Display.blit(self.__image, self.__coordinate)
