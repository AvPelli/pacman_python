from abc import ABC, abstractmethod
from copy import deepcopy

from Coordinate import Coordinate
from Direction import Direction


class Character(ABC):
    def __init__(self, PIXELSIZE, speed, moving_pos, direction, movable, moving_between_tiles, game_display, game,
                 coordinate):

        # protected variables for all the subclasses
        self._speed = speed
        self._PIXELSIZE = PIXELSIZE
        self._moving_pos = moving_pos
        self._direction = direction
        self._movable = movable
        self._moving_between_tiles = moving_between_tiles
        self._game = game
        self._game_display = game_display
        self._coord = coordinate
        self.start_coord = deepcopy(coordinate)

    # It wil draw a Character(image) of the given coordinate on the given game_display
    # Protected method: It can and only will be used in subclasses. Prohibited to be used outside these subclasses
    def _set_on_coord(self, coordinate, image):
        # self.check_reset()
        (xPixels, yPixels) = (coordinate.get_pixel_tuple())
        xPixels += self._direction.value[0] * self._moving_pos
        yPixels += self._direction.value[1] * self._moving_pos

        self._game_display.blit(image, (xPixels, yPixels))

    def check_reset(self):
        if self._direction is None:
            self._game.reset_chars()
            return

    @abstractmethod
    def move(self):
        pass

    def _set_on_opposite_side(self):
        (maxX, maxY) = self._game.get_max()
        (x, y) = (self._coord.get_coord_tuple())
        if x < 0:
            self._direction = Direction.LEFT
            self._coord = Coordinate(maxX - 1, y)
        elif x > maxX - 1:
            self._direction = Direction.RIGHT
            self._coord = Coordinate(0, y)

    # Calculates the next coordinate
    # Also this method checks if it is a "teleporter" which will perform __set_on_opposite_side() in move() method
    def _calculate_new_coord(self):
        (maxX, maxY) = self._game.get_max()
        (x, y) = (self._coord.get_coord_tuple())
        addX, addY = self._direction.value
        newX, newY = x + addX, y + addY
        jump = False
        if newX < 0 or newX > maxX - 1:
            jump = True
        return Coordinate(newX, newY), jump

    def reset_character(self):
        self._coord = self.start_coord
