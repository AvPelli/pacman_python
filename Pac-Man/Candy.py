import pygame as pg


class Candy:
    # Constructor for candy
    def __init__(self, game_Display, coordinate):
        self.__game_Display = game_Display
        self.__coord = coordinate
        self.__image = pg.image.load("res/candy/candy {number}.gif".format(number=0))


    # Draws the candy on a give coordinate
    def draw(self, coordinate):
        (xPixels, yPixels) = (coordinate.get_pixel_tuple())
        self.__game_Display.blit(self.__image, (xPixels, yPixels))

    """Getters"""

    # Getter, it returns the coordinate of this candy-object
    def get_coord(self):
        return self.__coord

    """Overwritten methods"""

    # Override the equals method
    # 2 Candy object are the same if they are located on the same coordinate
    def __eq__(self, other):
        if other == None or not isinstance(other, Candy):
            return False
        return self.__coord.get_x() == other.get_coord().get_x() and self.__coord.get_y() == other.get_coord().get_y()
