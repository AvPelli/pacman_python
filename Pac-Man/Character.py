from abc import ABC, abstractmethod
from Direction import Direction
from Coordinate import Coordinate

class Character(ABC):
    def __init__(self,PIXELSIZE,speed,moving_pos, direction,movable,moving_between_tiles,game_display,game,coordinate):

        #protected variables for all the subclasses
        self._speed = speed
        self._PIXELSIZE = PIXELSIZE
        self._moving_pos = moving_pos
        self._direction = direction
        self._movable = movable
        self._moving_between_tiles = moving_between_tiles
        self._game=game
        self._game_display=game_display
        self._coord=coordinate

    #It wil draw a Character(image) of the given coordinate on the given game_display
    #Protected method: It can and only will be used in subclasses. Prohibited to be used outside these subclasses
    def _set_on_coord(self, coordinate,image):
        (xPixels, yPixels) = (coordinate.get_pixel_tuple())
        xPixels += self._direction.value[0] * self._moving_pos
        yPixels += self._direction.value[1] * self._moving_pos

        self._game_display.blit(image, (xPixels, yPixels))

    @abstractmethod
    def move(self):
        pass

    def _set_on_opposite_side(self):
        (maxX, maxY) = self._game.get_max()
        (x, y) = (self._coord.get_coord_tuple())
        if x < 0:
            self._direction = Direction.LEFT
            self._coord = Coordinate(maxX, y)
        elif x > maxX:
            self._direction = Direction.RIGHT
            self._coord = Coordinate(-2, y)

    # Calculates the next coordinate
    # Also this method checks if it is a "teleporter" which will perform __set_on_opposite_side() in move() method
    def _calculate_new_coord(self):
        (maxX, maxY) = self._game.get_max()
        (x, y) = (self._coord.get_coord_tuple())
        addX, addY = self._direction.value
        newX, newY = x + addX, y + addY
        jump = False
        if newX < -1 or newX > maxX:
            jump = True
        return Coordinate(newX, newY), jump