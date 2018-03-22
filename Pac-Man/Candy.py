import pygame as pg


class Candy:
    # Constructor for candy
    def __init__(self, gameDisplay, coordinate):
        self.__gameDisplay = gameDisplay
        self.__coord = coordinate
        self.__image = pg.image.load("res/candy/candy {number}.gif".format(number=0))
        self.draw(coordinate)

    # Draws the candy on a give coordinate
    def draw(self, coordinate):
        (xPixels, yPixels) = (coordinate.get_pixel_tuple())
        self.__gameDisplay.blit(self.__image, (xPixels, yPixels))

    """Getters"""

    # Getter, it returns the coordinate of this candy-object
    def getCoord(self):
        return self.__coord

    """Overwritten methods"""

    # Override the equals method
    # 2 Candy object are the same if they are located on the same coordinate
    def __eq__(self, other):
        if other == None or not isinstance(other, Candy):
            return False
        return self.__coord.get_x() == other.getCoord().get_x() and self.__coord.get_y() == other.getCoord().get_y()
