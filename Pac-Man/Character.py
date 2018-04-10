from abc import ABC, abstractmethod
from Direction import Direction

class Character(ABC):
    def __init__(self,PIXELSIZE,speed,moving_pos, direction,movable,moving_between_tiles):
     if isinstance(direction,Direction) and isinstance(movable,bool) and isinstance(moving_between_tiles,bool):
        #protected variables for all the subclasses
        self._speed = speed
        self._PIXELSIZE = PIXELSIZE
        self._moving_pos = moving_pos
        self._direction = direction
        self._movable = movable
        self._moving_between_tiles = moving_between_tiles
     else:
         raise TypeError("Niet de juiste types")

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def set_on_opposite_side(self):
        pass
