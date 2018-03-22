import pygame as pg


class Candy:
    def __init__(self, gameDisplay, coordinate):
        self.__gameDisplay = gameDisplay
        self.__coord = coordinate
        self.__image = pg.image.load("res/candy/candy {number}.gif".format(number=0))
        self.draw(coordinate)

    def draw(self, coordinate):
        (xPixels, yPixels) = (coordinate.get_pixel_tuple())
        self.__gameDisplay.blit(self.__image, (xPixels, yPixels))

    def getCoord(self):
        return self.__coord

    def __eq__(self, other):
        if other == None or not isinstance(other, Candy):
            return False
        return self.__coord.get_x() == other.getCoord().get_x() and self.__coord.get_y() == other.getCoord().get_y()
