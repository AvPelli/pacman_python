import pygame as pg

from Coordinate import Coordinate
from Direction import Direction


class PacMan:
    def __init__(self, gameDisplay, coordinate, game):
        self.coord = coordinate
        self.gameDisplay = gameDisplay
        self.game = game
        self.nummer = 1
        self.direction = Direction.RIGHT
        self.image = pg.image.load(
            "res/pacman/pacman-{letter} {number}.gif".format(letter=self.direction.getLetter(), number=self.nummer))
        self.dict = self.makeDict()
        self.imageList = self.dict[self.direction.getLetter()]
        self.gameDisplay.blit(self.image, self.coord.getPixelTuple())
        self.score = 0

    def setOnCoord(self, coordinate):
        (xPixels, yPixels) = (coordinate.getPixelTuple())
        self.image = pg.image.load(self.imageList[self.nummer])
        self.gameDisplay.blit(self.image, (xPixels, yPixels))

    def setDirection(self, direction):
        self.direction = direction
        self.imageList = self.dict[direction.getLetter()]
        # self.nummer = 0

    def move(self):
        (x, y) = (self.coord.getCoordTuple())
        addX, addY = self.direction.value
        newX, newY = x + addX, y + addY
        self.coord = Coordinate(newX, newY)
        self.setOnCoord(self.coord)
        self.nummer = (self.nummer + 1) % 8
        candys = self.game.getCandy()
        for candy in candys:
            if self.coord == candy.getCoord():
                self.game.getCandy().remove(candy)
                self.score += 1
                print("Score = {score}".format(score=self.score))
                return

    def makeDict(self):
        dict = {}
        for letter in "ldru":
            dict[letter] = list()
            for i in range(1, 10):
                dict[letter].append("res/pacman/pacman-{letter} {number}.gif".format(letter=letter, number=i))

        return dict
