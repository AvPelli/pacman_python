class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.PIXELSIZE = 26

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getPixelTuple(self):
        # Formule voor van coord systeem --> naar pixels
        return self.x * self.PIXELSIZE, self.y * self.PIXELSIZE

    def getCoordTuple(self):
        return self.x, self.y

    def __eq__(self, other):
        if other == None or not isinstance(other, Coordinate):
            return False
        return self.x == other.getX() and self.y == other.getY()

