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
        self.astar = Astar(game.get_gates(), self._game.get_pacman())
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

    def move(self, scatter):
        if self._moving_between_tiles:
            self.__move_between_tiles()
        else:
            if not scatter:
                check_next_coord, jump = self._calculate_new_coord()
                if check_next_coord in self.walls:
                    self._direction = self.astar.get_direction(self._coord,
                                                               self.astar.get_closest_tile(self.__update_target_tile()))

                if self.__check_neighbours() == True:
                    self._direction = self.astar.get_direction(self._coord,
                                                               self.astar.get_closest_tile(self.__update_target_tile()))

                if jump:
                    self._set_on_opposite_side()
                self._moving_between_tiles = True

                self.check_frightened()
                self._draw_character(self._coord, self.__image)

            if self.__frightened:
                check_next_coord, jump = self._calculate_new_coord()
                if check_next_coord in self.walls:
                    self._direction = self.astar.get_direction(self._coord, self.astar.get_closest_tile(
                        self.__update_target_tile()))

                if self.__check_neighbours() == True:
                    self._direction = self.astar.get_direction(self._coord, self.astar.get_closest_tile(
                        self.__update_target_tile()))

            else:
                check_next_coord, jump = self._calculate_new_coord()
                if check_next_coord in self.walls:
                    self._direction = self.astar.get_direction(self._coord, self.astar.get_closest_tile(
                        self.__update_target_tile_scatter()))

                if self.__check_neighbours() == True and check_next_coord != self._game.get_pacman_coord:
                    self._direction = self.astar.get_direction(self._coord, self.astar.get_closest_tile(
                        self.__update_target_tile_scatter()))

            if jump:
                self._set_on_opposite_side()
            self._moving_between_tiles = True
            self.check_frightened()
            self._draw_character(self._coord, self.__image)

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
            pac_x, pac_y = pac_coord.get_coord_tuple()
            blinky_x, blinky_y = blinky_coord.get_coord_tuple()
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

    def __update_target_tile_scatter(self):
        if self.__id == 0:
            self.__target_tile = Coordinate(21, 23)
        elif self.__id == 1:
            self.__target_tile = Coordinate(21, 23)
        elif self.__id == 2:
            self.__target_tile = Coordinate(21, 23)
        elif self.__id == 3:
            self.__target_tile = Coordinate(21, 23)

        self.__target_tile = self.astar.get_closest_tile(self.__target_tile)
        return self.__target_tile

    def calculate_direction(self):
        pass  # voor nu

    def __check_neighbours(self):
        horizontal = False
        vertical = False
        x, y = self._coord.get_coord_tuple()
        if Coordinate(x - 1, y) not in self.walls or Coordinate(x + 1, y) not in self.walls:
            horizontal = True
        if Coordinate(x, y + 1) not in self.walls or Coordinate(x, y - 1) not in self.walls:
            vertical = True
        return horizontal and vertical

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
