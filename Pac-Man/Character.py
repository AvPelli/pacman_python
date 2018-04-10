from abc import ABC, abstractmethod

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

    @abstractmethod
    def set_on_opposite_side(self):
        pass

