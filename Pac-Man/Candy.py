import pygame as pg


class Candy:

    def __init__(self, game_display, coordinate):
        """
        Constructor of Candy\n
        :param game_display:
        :param coordinate: type: Coordinate
        """
        self._game_Display = game_display
        self._coord = coordinate
        self._image = pg.image.load("res/candy/candy {number}.gif".format(number=0))
        self._score = 10

    def draw(self, coordinate):
        """
        Draws this object (Candy) on the given coordinate.\n
        :param coordinate: type: Coordinate
        :return: void
        """
        (xPixels, yPixels) = (coordinate.get_pixel_tuple())
        self._game_Display.blit(self._image, (xPixels, yPixels))

    """Getters"""

    def get_coord(self):
        """
        It returns the coordinate of this candy-object.\n
        :return: Coordinate
        """
        return self._coord

    def get_score(self):
        """
        It returns the score the player will get if he eats a Candy Object.\n
        :return: int
        """
        return self._score

    """Overwritten methods"""

    def __eq__(self, other):
        """
        Override the equals method:\n
        2 Candy object are the same if they are located on the same coordinate.\n
        :param other: type: Coordinate
        :return: int (boolean)
        """
        if other is None or not isinstance(other, Candy):
            return False
        return self._coord.get_x() == other.get_coord().get_x() and self._coord.get_y() == other.get_coord().get_y()
