import pygame as pg

from Character import Character
from Coordinate import Coordinate
from Direction import Direction
from Candy import Candy
from Fruit import Fruit


class FruitSelector:
    def __init__(self, game_Display):
        self._game_Display = game_Display
        self.__names = {"Cherry": 60, "Apple": 90, "Strawberry": 120, "Orange": 150, "Green Melon": 180}
        self.__images = {}
        # self.__fruitcoord = Coordinate(232, 320)
        self.__level = 1
        # self.__starttimer = pg.time.get_ticks()
        self.__time = 0

    def calc_until_fruit(self, candiesleft,level):
        self.__level = level
        if candiesleft < 500:
            # self, game_Display, coordinate, fruitselector, fruittype
            fruit = Fruit(self._game_Display, (216, 320), self, "Cherry")
            self._game_Display.blit(pg.image.load("res/fruit/Cherry2.png"), (384, 544))
            fruit.draw()

    def get_fruitbonus(self, fruitname):
        return self.__names[fruitname]

    def get_fruitcoord(self):
        return self.__fruitcoord

    def get_level(self, level):
        self.__level = level

    def set_level(self, level):
        self.__level = level
