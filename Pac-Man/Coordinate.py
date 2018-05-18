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
        Checks if Coordinate is a wall
        :return: boolean
        """
        return self.__is_wall

    def get_x(self):
        """
        Getter
        :return: x Coordinate
        """
        return self.__x

    def get_y(self):
        """
        Getter
        :return: y Coordinate
        """
        return self.__y

    def get_pixel_tuple(self):
        """
        Getter
        :return: tuple (Pixel x, Pixel y)
        """
        # Formule voor van coord systeem --> naar pixels
        return int((self.__x * self.__PIXELSIZE)), int(
            (self.__y * self.__PIXELSIZE) + 3 * self.__PIXELSIZE)

    def get_coord_tuple(self):
        """
        Getter
        :return: tuple (Coordinate X, Coordinate Y)
        """
        return self.__x, self.__y

    """Overwritten methods"""

    def __eq__(self, other):
        """
        Override the equal methode 2 Coordinate objects are the same if x and y of both objects are the same
        :return: string
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
