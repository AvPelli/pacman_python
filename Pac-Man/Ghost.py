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
        self._direction = Direction.UP
        self.imagechooser()
        self.__update_target_tile()

        self.__frightened = False
        self.__frightenedimg = 1

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
        if self._moving_between_tiles:
            self.__move_between_tiles()
        else:
            check_next_coord, jump = self._calculate_new_coord()
            if check_next_coord in self.walls:
                self._direction = self.astar.get_direction(self._coord,
                                                           self.astar.get_closest_tile(self.__update_target_tile()))
                self.check_direction()
            if self.__check_neighbours() == True:
                self._direction = self.astar.get_direction(self._coord,
                                                           self.astar.get_closest_tile(self.__update_target_tile()))
                self.check_direction()
            if jump:
                self._set_on_opposite_side()
            self._moving_between_tiles = True
            self.check_direction()
            self.check_frightened()
            self._draw_character(self._coord, self.__image)

    def check_direction(self):
        if self._direction is None:
            self._speed = 0

    def __move_between_tiles(self):
        # Proceed to the next tile
        super()._move_between_tiles()
        self._draw_character(self._coord, self.__image)

    def __update_target_tile(self):
        pac_coord = self._game.get_pacman_coord()
        pac_direction = self._game.get_pacman_direction()
        if self.__id == 0:
            self.__target_tile = pac_coord
        elif self.__id == 1:
            for i in range(4):
                pac_coord.update_coord(pac_direction)
            self.__target_tile = pac_coord
        elif self.__id == 2:
            for i in range(2):
                pac_coord.update_coord(pac_direction)
            blinky_coord = (self._game.get_ghosts()[0]).get_coord()
            pac_x = pac_coord.get_x()
            pac_y = pac_coord.get_y()
            blinky_x = blinky_coord.get_x()
            blinky_y = blinky_coord.get_y()
            x_diff = pac_x - blinky_x
            y_diff = pac_y - blinky_y
            # aanpassen als move en calculate_direction beter geschreven zijn maar voor nu:

            self.__target_tile = Coordinate(blinky_x + 2 * x_diff, blinky_y + 2 * y_diff)

        else:
            if self.astar.manhattan_distance(pac_coord.get_coord_tuple(), self._coord.get_coord_tuple()) < 10:
                self.__target_tile = Coordinate(15, 15)
            else:
                self.__target_tile = pac_coord

            # aanpassen
        self.__target_tile = self.astar.get_closest_tile(self.__target_tile)
        return self.__target_tile

    def calculate_direction(self):
        pass  # voor nu

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
        self._coord = coord

    def set_frightened(self, value):
        self.__frightened = value

    def check_frightened(self):
        if self.__frightened:
            self.go_frightened()

    def go_frightened(self):
        if self.__frightenedimg == 1:
            self.__image = pg.image.load("res/pacmanghost/bluepacman.png")
            self.__frightenedimg = self.__frightenedimg + 1
        elif self.__frightenedimg == 2:
            self.__image = pg.image.load("res/pacmanghost/bluepacman2.png")
            self.__frightenedimg = 1

    def reset_character(self):
        super().reset_character()
        self._direction = Direction.UP
        self._draw_character(self.start_coord, self.__image)
