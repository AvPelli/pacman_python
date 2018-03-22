import pygame as pg

from Coordinate import Coordinate
from Direction import Direction


class PacMan:
    def __init__(self, gameDisplay, coordinate, game, walls):
        self.__coord = coordinate
        self.__gameDisplay = gameDisplay
        self.__game = game
        self.__nummer = 1
        self.__direction = Direction.RIGHT
        self.__image = pg.image.load(
            "res/pacman/pacman-{letter} {number}.png".format(letter=self.__direction.getLetter(), number=self.__nummer))
        self.dict = self.__image_dict()
        self.imageList = self.dict[self.__direction.getLetter()]
        self.__gameDisplay.blit(self.__image, self.__coord.get_pixel_tuple())
        self.score = 0
        self.moveable = True
        self.walls = walls
        self.possNext = None

    def set_direction(self, direction):
        if Coordinate(self.__coord.get_x() + direction.value[0],
                      self.__coord.get_y() + direction.value[1]) in self.walls:
            self.possNext = direction
            return
        self.possNext = None
        self.__direction = direction
        self.moveable = True

    def move(self):
        if not self.moveable:
            self.__set_on_coord(self.__coord)
            return
        self.__direction_waiter()
        new_coord = self.__get_new_coord()
        if new_coord in self.walls:
            self.moveable = False
        else:
            self.__coord = new_coord

        self.__set_on_coord(self.__coord)

        self.__eat_candy()

    def __set_on_coord(self, coordinate):
        (xPixels, yPixels) = (coordinate.get_pixel_tuple())
        self.__image = self.__get_image_direction(self.__direction)
        self.__gameDisplay.blit(self.__image, (xPixels, yPixels))
        print(coordinate)

    def __direction_waiter(self):
        if self.possNext is not None and Coordinate(self.__coord.get_x() + self.possNext.value[0],
                                                    self.__coord.get_y() + self.possNext.value[1]) not in self.walls:
            self.__direction = self.possNext

    def __eat_candy(self):
        candies = self.__game.get_candy_dict()
        if self.__coord in candies.keys():
            del self.__game.get_candy_dict()[self.__coord]
            self.score += 1

    def __get_new_coord(self):
        (maxX, maxY) = self.__game.get_max()
        (x, y) = (self.__coord.get_coord_tuple())
        addX, addY = self.__direction.value
        newX, newY = x + addX, y + addY
        if newX < -1:
            newX = maxX - 1
            self.__direction = Direction.LEFT
            self.possNext = self.__direction
        elif newX >= maxX - 1:
            newX = -1
            self.__direction = Direction.RIGHT
            self.possNext = self.__direction
        return Coordinate(newX, newY)

    def __image_dict(self):
        dict = {}
        for letter in "ldru":
            dict[letter] = list()
            for i in range(1, 10):
                dict[letter].append("res/pacman/pacman-{letter} {number}.png".format(letter=letter, number=i))
        return dict

    def __get_image_direction(self, direction):
        self.__nummer = (self.__nummer + 1) % 8
        return pg.image.load(self.dict[direction.getLetter()][self.__nummer])
