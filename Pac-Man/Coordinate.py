class Coordinate:
    # Constructor of Coordinate
    def __init__(self, x, y, is_wall=False):
        """
        Creates Coordinate object, each coordinate also holds a boolean that tells if the coordinate is a wall or not.
        :param: x (Coordinate)
        :param: y (Coordinate)
        :param: is_wall : boolean
        :return: void
        """
        self.__x = x
        self.__y = y
        self.__PIXELSIZE = 16
        self.__is_wall = is_wall

    def update_coord(self, direction):
        self.__x += direction.value[0]
        self.__y += direction.value[1]

    """Getters"""

    def is_wall(self):
        """
        Returns if this coordinate is a wall
        :return: boolean
        """
        return self.__is_wall

    def get_x(self):
        """
        Returns x value of this coordinate
        :return: x Coordinate
        """
        return self.__x

    def get_y(self):
        """
        Returns y value of this coordinate
        :return: y Coordinate
        """
        return self.__y

    def get_pixel_tuple(self):
        """
        Returns a tuple of the pixels of this coordinate (Pixel x, Pixel y)
        :return: tuple
        """
        # Formula to go from the coord system to pixel system (x, y) --> (pixel_x, pixel_y)
        return int((self.__x * self.__PIXELSIZE)), int(
            (self.__y * self.__PIXELSIZE) + 3 * self.__PIXELSIZE)

    def get_coord_tuple(self):
        """
        Returns a tuple of the x, y -value of this coordinate (x, y)
        :return: tuple
        """
        return self.__x, self.__y

    """Overwritten methods"""

    def __eq__(self, other):
        """
        Override the equal method 2 Coordinate objects are the same if x and y of both objects are the same
        :return: int (boolean)
        """
        if not isinstance(other, Coordinate):
            return False
        return self.__x == other.get_x() and self.__y == other.get_y()

    def __hash__(self) -> int:
        """
        Override the hashcode this is needed for dicitionaries like the candy dictionary
        :return: int
        """
        return (int)(self.__x * 31 + self.__y * 7 + 1)

    def __str__(self) -> str:
        """
        to string method of Coordinate
        :return: string
        """
        return "Coordinate: X: {x},   Y: {y}".format(x=self.__x, y=self.__y)
