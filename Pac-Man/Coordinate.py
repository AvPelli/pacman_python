class Coordinate:
    # Constructor of Coordinate
    def __init__(self, x, y, is_wall=False):
        self.__x = x
        self.__y = y
        self.__PIXELSIZE = 16
        self.__is_wall = is_wall

    def update_coord(self, direction):
        self.__x += direction.value[0]
        self.__y += direction.value[1]

    """Getters"""

    # Getter: returns if there is a wall on this coordinate
    def is_wall(self):
        return self.__is_wall

    # Getter: returns x value
    def get_x(self):
        return self.__x

    # Getter: returns y value
    def get_y(self):
        return self.__y

    # Getter: returns a tuple (Pixel X, Pixel Y)
    def get_pixel_tuple(self):
        # Formule voor van coord systeem --> naar pixels
        return int((self.__x * self.__PIXELSIZE)), int(
            (self.__y * self.__PIXELSIZE) + 3 * self.__PIXELSIZE)

    # Getter: returns a tuple (X, Y)
    def get_coord_tuple(self):
        return self.__x, self.__y

    """Overwritten methods"""

    # Override the equal methode
    # 2 Coordinate objects are the same if x and y of both objects are the same
    def __eq__(self, other):
        if not isinstance(other, Coordinate):
            return False
        return self.__x == other.get_x() and self.__y == other.get_y()

    # Override the hashcode
    # This is needed for dicitionaries like the candy dictionary
    def __hash__(self) -> int:
        return (int)(self.__x * 31 + self.__y * 7 + 1)

    # to string method of Coordinate
    def __str__(self) -> str:
        return "Coordinate: X: {x},   Y: {y}".format(x=self.__x, y=self.__y)
