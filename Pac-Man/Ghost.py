import pygame as pg

from Character import Character
from Coordinate import Coordinate
from Direction import Direction
from Astar import Astar

class Ghost(Character):
    ghost_id = 0
    astar = Astar()

    def __init__(self, game_display, coordinate, game, walls):
        # Start variables
        super().__init__(PIXELSIZE=16, speed=2, moving_pos=0,
                         direction=Direction.UP, movable=True,
                         moving_between_tiles=False, game_display=game_display,
                         game=game, coordinate=coordinate)


        self.walls = walls
        self.__id = Ghost.ghost_id
        Ghost.ghost_id += 1
        Ghost.ghost_id %= 4
        self._speed = (16 - self.__id)/8.0
        self.imagechooser()

    def imagechooser(self):
        if self.__id == 0:
            self.__image = pg.image.load("res/ghost/inky/start.png")
        elif self.__id == 1:
            self.__image = pg.image.load("res/ghost/blinky/start.png")
        elif self.__id == 2:
            self.__image = pg.image.load("res/ghost/clyde/start.png")
        elif self.__id == 3:
            self.__image = pg.image.load("res/ghost/pinky/start.png")


    def move(self):
        if self._moving_between_tiles:
            self.__move_between_tiles()
        else:

            check_next_coord, jump = self._calculate_new_coord()
            if check_next_coord in self.walls:
                self._direction = Ghost.astar.get_direction(self._direction, self._coord,
                                                            self.__calculate_target_tile())
            if self.__check_neighbours() == True:
                self._direction = Ghost.astar.get_direction(self._direction, self._coord, self.__calculate_target_tile())
            if jump:
                self._set_on_opposite_side()
            self._moving_between_tiles = True
            self._set_on_coord(self._coord, self.__image)


    def __move_between_tiles(self):
        # Proceed to the next tile
        self._moving_pos += self._speed
        if self._moving_pos >= 16:
            self._moving_pos = 0
            self._moving_between_tiles = False
            # Once there, it's coordinate will be updated so it's ready to be checked in the else: part of move
            self._coord.update_coord(self._direction)
        self._set_on_coord(self._coord, self.__image)

    def __calculate_target_tile(self):
        return self._game.get_pacman_coord()

    def __check_neighbours(self):
        horizontal = False
        vertical = False
        x = self._coord.get_x()
        y = self._coord.get_y()
        if Coordinate(x -1, y) not in self.walls:
            horizontal = True
        if Coordinate(x +1, y) not in self.walls:
            horizontal = True
        if Coordinate(x, y+1) not in self.walls:
            vertical = True
        if Coordinate(x, y-1) not in self.walls:
            vertical = True
        return horizontal and vertical
