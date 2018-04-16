import pygame as pg

from Character import Character
from Coordinate import Coordinate
from Direction import Direction

class Ghost(Character):
    ghost_id = 0

    def __init__(self, game_display, coordinate, game, walls):
        # Start variables
        super().__init__(PIXELSIZE=16, speed=2, moving_pos=0,
                         direction=Direction.RIGHT, movable=True,
                         moving_between_tiles=False, game_display=game_display,
                         game=game, coordinate=coordinate)
        self.__image = pg.image.load("res/vijand.png")
        self.walls = walls
        self.__id = self.ghost_id
        Ghost.ghost_id += 1
        Ghost.ghost_id %= 4
        print(self.__id)

    def move(self):
        self._set_on_coord(self._coord, self.__image)