from abc import ABC, abstractmethod
from copy import deepcopy

from Coordinate import Coordinate
from Direction import Direction


class Character(ABC):
    def __init__(self, PIXELSIZE, speed, moving_pos, direction, game, coordinate):
        """
        Creates a Character object, Ghost and Pacman subclasses also use the variables here, so they are protected.
        :return: void
        """
        # protected variables for all the subclasses
        self._speed = speed
        self._PIXELSIZE = PIXELSIZE
        self._moving_pos = moving_pos
        self._direction = direction
        self._movable = True
        self._moving_between_tiles = False
        self._game = game
        self._coord = coordinate
        self.start_coord = deepcopy(coordinate)

    def _draw_character(self, coordinate, image):
        """
        Draw a Character(image) of the given coordinate on the given game_display
        Protected method: It can and only will be used in subclasses. Prohibited to be used outside these subclasses
        :param: Coordinate: where to draw the object
        :param: image: what image to draw
        :return: void
        """
        (xPixels, yPixels) = (coordinate.get_pixel_tuple())
        # self.check_reset()
        if self._direction is not None:
            xPixels += self._direction.value[0] * self._moving_pos
            yPixels += self._direction.value[1] * self._moving_pos
        self._game.get_game_display().blit(image, (xPixels, yPixels))

    @abstractmethod
    def move(self):
        pass

    def _move_between_tiles(self):
        """
        Method used for character while they move between tiles (Base model of the method)
        each subclass expands this method
        :return: void
        """
        self._moving_pos += self._speed
        if self._moving_pos >= 16:
            self._moving_pos = 0
            self._moving_between_tiles = False
            # Once there, it's coordinate will be updated so it's ready to be checked in the else: part of move
            self._coord.update_coord(self._direction)

    def _set_on_opposite_side(self):
        """
        Set the character on the other side
        :return: void
        """
        (maxX, maxY) = self._game.get_max()
        (x, y) = (self._coord.get_coord_tuple())

        if x <= 0:
            self._direction = Direction.LEFT
            self._coord = Coordinate(maxX, y)
        elif x >= maxX:
            self._direction = Direction.RIGHT
            self._coord = Coordinate(0, y)

    def _calculate_new_coord(self):
        """
        Calculates the next coordinate also this method checks if it is a "teleporter"
        which will perform __set_on_opposite_side() in move() method
        :return: Coordinate
        """
        (maxX, maxY) = self._game.get_max()
        (x, y) = (self._coord.get_coord_tuple())
        addX, addY = self._direction.value
        newX, newY = x + addX, y + addY
        jump = False
        if newX < 0 or newX > maxX or newX > 0 and x == 0 or newX < maxX and x == maxX:
            jump = True
            newX, newY = 0, 0
        return (newX, newY), jump

    def reset_character(self):
        """
        Base model of a method that reset the character to the begin status
        :return: void
        """
        # deepcopy, or else the attribute __coord will be a reference to the attribute start_coord
        # this way when pacman gets caught the second time, it will "reset" to the coordinate it already stands on
        self._coord = deepcopy(self.start_coord)

    def get_coord(self):
        """
        Getter
        :return: Coordinate
        """
        return deepcopy(self._coord)

    def get_direction(self):
        """
        Getter
        :return: Direction
        """
        return deepcopy(self._direction)

    def set_speed(self, speedvalue):
        self._speed = speedvalue
