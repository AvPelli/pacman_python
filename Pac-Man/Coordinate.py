class Coordinate:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__PIXELSIZE = 16

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_pixel_tuple(self):
        # Formule voor van coord systeem --> naar pixels
        return (self.__x * self.__PIXELSIZE) + 1 * self.__PIXELSIZE, (
            self.__y * self.__PIXELSIZE) + 4 * self.__PIXELSIZE

    def get_coord_tuple(self):
        return self.__x, self.__y

    def __eq__(self, other):
        if other == None or not isinstance(other, Coordinate):
            return False
        return self.__x == other.get_x() and self.__y == other.get_y()

    def __str__(self) -> str:
        return "X: {x},   Y: {y}".format(x=self.__x, y=self.__y)

    def __hash__(self) -> int:
        return (int)(self.__x * 31 + self.__y * 7 + 1)
