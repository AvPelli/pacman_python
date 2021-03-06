import pygame as pg


class Fruit:
    def __init__(self, game_display, coordinate, fruitselector, fruittype):
        """
        Creates Fruit Object. \n
        A fruit is a special kind of food that can be eaten for extra points, but it only occurs within a specific\n
        time window on every level. For more information about this, see FruitSelector.\n
        :param game_display: The display to which the fruit object is drawn.
        :param coordinate: type: Coordinate: Where the fruit is drawn
        :param fruitselector: type: FruitSelector: The FruitSelector that manages this Fruit
        :param fruittype: Which kind of fruit this is.
        """
        self.__game_display = game_display
        self.__image = pg.image.load("res/fruit/" + fruittype + ".png")
        self.__coordinate = coordinate
        self.__fruittype = fruittype
        self._fruitselector = fruitselector
        self.__bonus = self._fruitselector.get_fruitbonus(self.__fruittype)
        self.__eaten = False

    """Draw Method"""

    def draw(self):
        """
        This method draws the fruit on it's coordinate. To appear in the middle, 8 extra pixels are added\n
        to its pixelcoordinate before drawing.\n
        :return: void
        """
        coord_pixels = self.__coordinate.get_pixel_tuple()
        res = coord_pixels[0] + 8, coord_pixels[1]
        self.__game_display.blit(self.__image, res)

    """Getters"""

    def get_fruit_name(self):
        """
        This method returns the fruit type. Needed by FruitSelector to determine its score.\n
        :return: String
        """
        return self.__fruittype

    def get_score(self):
        """
        This method returns its score, this method is only called when Pacman eats the Fruit. Therefore it will also set\n
        the __eaten boolean.\n
        :return: int
        """
        if not self.__eaten:
            self.__eaten = True
            return self.__bonus
        else:
            return 0

    def get_eaten(self):
        """
        This method returns the __eaten boolean which is used by FruitSelector.\n
        :return: boolean
        """
        return self.__eaten
