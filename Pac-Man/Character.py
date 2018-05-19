from abc import ABC, abstractmethod
from copy import deepcopy

from Coordinate import Coordinate
from Direction import Direction


class Character(ABC):
    def __init__(self, PIXELSIZE, speed, moving_pos, direction, game, coordinate):
        """
        Creates a Character object, Ghost and Pacman subclasses also use the variables here, so they are protected.
        :param PIXELSIZE: type: int
        :param speed: type: int
        :param moving_pos: type: int
        :param direction:  type: Direction
        :param game:  type: Game
        :param coordinate:  type: Coordinate
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
        :param: coordinate:  type: Coordinate:  where to draw the object
        :param: image: what image to draw
        :return: void
        """
        (xPixels, yPixels) = (coordinate.get_pixel_tuple())
        if self._direction is not None:
            xPixels += self._direction.value[0] * self._moving_pos
            yPixels += self._direction.value[1] * self._moving_pos
        self._game.get_game_display().blit(image, (xPixels, yPixels))

    @abstractmethod
    def move(self):
        """
        Abstract method move, subclasses will have its own implementation of this method
        :return: void
        """
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
        :return: Coordinate, boolean
        """
        (max_x, max_y) = self._game.get_max()
        (x, y) = (self._coord.get_coord_tuple())
        add_x, add_y = self._direction.value
        new_x, new_y = x + add_x, y + add_y
        jump = False
        if new_x < 0 or new_x > max_x or new_x > 0 and x == 0 or new_x < max_x and x == max_x:
            jump = True
            new_x, new_y = 0, 0
        return (new_x, new_y), jump

    def reset_character(self):
        """
        Base model of a method that reset the character to the begin status
        :return: void
        """
        # Deepcopy, or else the attribute __coord will be a reference to the attribute start_coord
        # This way when pacman gets caught the second time, it will "reset" to the coordinate it already stands on
        self._coord = deepcopy(self.start_coord)

    def set_coord(self, coordinate):
        """
        Sets the Character's coordinate, used when resetting characters between levels
        :param coordinate: what it will be set to
        :return: void
        """
        self._coord = coordinate

    """Getters"""

    def get_coord(self):
        """
        Returns the coordinate of the Character
        :return: Coordinate
        """
        # Deepcopy, for elimination of a privacy leak
        return deepcopy(self._coord)

    def get_direction(self):
        """
        Returns the direction the character is going in
        :return: Direction
        """
        # Deepcopy, for elimination of a privacy leak
        return deepcopy(self._direction)

    """Setters"""

    def set_speed(self, speedvalue):
        """
        Sets the speed of the character to the given speedvalue
        :param speedvalue: type: int
        :return: void
        """
        self._speed = speedvalue
