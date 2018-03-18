import pygame as pg


class Candy:
    def __init__(self, gameDisplay, coordinate):
        self.gameDisplay = gameDisplay
        self.coord = coordinate
        self.image = pg.image.load("res/candy/candy {number}.gif".format(number=0))
        self.draw(coordinate)

    def draw(self, coordinate):
        (xPixels, yPixels) = (coordinate.getPixelTuple())
        self.gameDisplay.blit(self.image, (xPixels, yPixels))

    def getCoord(self):
        return self.coord

    def __eq__(self, other):
        if other == None or not isinstance(other, Candy):
            return False
        return self.coord.getX() == other.getCoord().getX() and self.coord.getY() == other.getCoord().getY()
