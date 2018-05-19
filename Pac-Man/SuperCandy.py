import pygame as pg

from Candy import Candy


class SuperCandy(Candy):
    def __init__(self, game_display, coordinate):
        """
        Constructor of SuperCandy, a subclass of Candy:\n
        When eaten it allows the player to start frightened mode and he can start eating the ghosts.\n
        :param game_display:
        :param coordinate: type: Coordinate
        """
        super().__init__(game_display, coordinate)
        self._image = pg.image.load("res/candy/superdot.png")
        self.__score = 100

    def get_score(self):
        """
        Returns the score the player gets, when he eats a SuperCandy object.\n
        :return: int
        """
        return self.__score
