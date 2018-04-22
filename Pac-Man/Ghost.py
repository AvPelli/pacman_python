import pygame as pg

from Astar import Astar
from Character import Character
from Coordinate import Coordinate
from Direction import Direction


class Ghost(Character):
    ghost_id = 0

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
        self._speed = (16 - self.__id) / 8.0
        self.astar = Astar(game.get_gates())
        self._direction = self.astar.get_direction(self._coord, self.__calculate_target_tile())
        self.imagechooser()

    def imagechooser(self):
        if self.__id == 2:
            self.__image = pg.image.load("res/ghost/inky/start.png")
        elif self.__id == 0:
            self.__image = pg.image.load("res/ghost/blinky/start.png")
        elif self.__id == 3:
            self.__image = pg.image.load("res/ghost/clyde/start.png")
        elif self.__id == 1:
            self.__image = pg.image.load("res/ghost/pinky/start.png")

    def move(self):
        self._speed = (16 - self.__id) / 8.0
        if self._moving_between_tiles:
            self.__move_between_tiles()
        else:
            check_next_coord, jump = self._calculate_new_coord()
            if check_next_coord in self.walls:
                self._direction = self.astar.get_direction(self._coord, self.__calculate_target_tile())
                self.check_direction()
            if self.__check_neighbours() == True:
                self._direction = self.astar.get_direction(self._coord, self.__calculate_target_tile())
                self.check_direction()
            if jump:
                self._set_on_opposite_side()
            self._moving_between_tiles = True
            self.check_direction()
            self._draw_character(self._coord, self.__image)

    def check_direction(self):
        if self._direction is None:
            self._speed = 0

    def __move_between_tiles(self):
        # Proceed to the next tile
        super()._move_between_tiles()
        self._draw_character(self._coord, self.__image)

    def __calculate_target_tile(self):
        return self._game.get_pacman_coord()

    def __check_neighbours(self):
        amount = 0
        x, y = self._coord.get_coord_tuple()
        for dir in Direction:
            if Coordinate(x + dir.value[0], y + dir.value[1]) not in self.walls:
                amount += 1
        return amount >= 2

    def get_coord(self):
        return self._coord

    def set_coord(self, coord):
        self.__coord = coord

    def reset_character(self):
        super().reset_character()
        self._direction = Direction.UP
        self._draw_character(self.start_coord, self.__image)
