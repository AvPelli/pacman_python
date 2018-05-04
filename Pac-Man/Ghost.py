import pygame as pg

from Astar import Astar
from Character import Character
from Coordinate import Coordinate
from Direction import Direction


class Ghost(Character):
    ghost_id = 0
    neighbours_map = {}

    def __init__(self, game, coordinate, coord_dict):
        # Start variables
        super().__init__(PIXELSIZE=16, speed=2, moving_pos=0, direction=Direction.UP, game=game, coordinate=coordinate)

        self.__coord_dict = coord_dict
        self.__id = Ghost.ghost_id
        Ghost.ghost_id += 1
        Ghost.ghost_id %= 4
        self._speed = (16 - self.__id) / 8.0
        self.astar = Astar(self._game.get_map().get_gates(), self._game.get_pacman())
        self._direction = Direction.UP
        self.imagechooser()
        self.__update_target_tile()

        self.__frightened = False
        self.__frightenedimg = 1

        self.__eaten = False
        self.__movestart = False

        self.__scatter_state = 0
        # blinky scattercoordinates
        self.blinky_dict = {0: Coordinate(21, 5), 1: Coordinate(26, 5), 2: Coordinate(26, 1), 3: Coordinate(21, 1)}
        # pinky scattercoordinates
        self.pinky_dict = {0: Coordinate(6, 5), 1: Coordinate(6, 1), 2: Coordinate(1, 1), 3: Coordinate(1, 5)}
        # inky scattercoordinates
        self.inky_dict = {0: Coordinate(19, 23), 1: Coordinate(26, 29), 2: Coordinate(16, 29)}
        # clyde scattercoordinates
        self.clyde_dict = {0: Coordinate(7, 23), 1: Coordinate(1, 29), 2: Coordinate(12, 29)}

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
        elif (self.get_gostart()):
            self.move_to_start()
        else:
            check_next_coord, jump = self._calculate_new_coord()
            if self.__coord_dict.get(check_next_coord).is_wall():
                self._direction = self.astar.get_direction(self._coord,
                                                           self.astar.get_closest_tile(self.__update_target_tile()))

            if self.__check_neighbours() == True:
                self._direction = self.astar.get_direction(self._coord,
                                                           self.astar.get_closest_tile(self.__update_target_tile()))

            # check if frightened
            elif self.__frightened:
                if self.__coord_dict.get(check_next_coord).is_wall():
                    self._direction = self.astar.get_direction(self._coord, self._coord)

                if self.__check_neighbours() == True:
                    self._direction = self.astar.get_direction(self._coord, self._coord)

            if jump:
                self._set_on_opposite_side()
            self._moving_between_tiles = True
            self.check_frightened()
            self._draw_character(self._coord, self.__image)

    def scatter(self):
        if self._moving_between_tiles:
            self.__move_between_tiles()
        elif (self.get_gostart()):
            self.move_to_start()
        else:
            check_next_coord, jump = self._calculate_new_coord()
            self.__update_target_tile_scatter()

            if self.__coord_dict.get(check_next_coord).is_wall():
                path = self.astar.find_path(self._coord, self.__target_tile)
                self._direction = self.astar.dictionary[path[0]]

            if self.__check_neighbours() == True:
                path = self.astar.find_path(self._coord, self.__target_tile)
                self._direction = self.astar.dictionary[path[0]]

            if jump:
                self._set_on_opposite_side()
            self._moving_between_tiles = True
            self.check_frightened()
            self._draw_character(self._coord, self.__image)

    def frightened(self):
        if self._moving_between_tiles:
            self.__move_between_tiles()
        elif (self.get_gostart()):
            self.move_to_start()
        else:
            check_next_coord, jump = self._calculate_new_coord()
            if self.__coord_dict.get(check_next_coord).is_wall():
                self._direction = self.astar.get_direction(self._coord,
                                                           self.astar.get_closest_tile(self.__update_target_tile()))

            if self.__check_neighbours() == True:
                self._direction = self.astar.get_direction(self._coord,
                                                           self.astar.get_closest_tile(self.__update_target_tile()))

            # frightened mode: random movement
            if self.__coord_dict.get(check_next_coord).is_wall():
                self._direction = self.astar.choose_random(self._coord)

            if self.__check_neighbours() == True:
                self._direction = self.astar.choose_random(self._coord)

            if jump:
                self._set_on_opposite_side()
            self._moving_between_tiles = True
            self.check_frightened()
            self._draw_character(self._coord, self.__image)

    def move_to_start(self):
        # Unlike scatter(), frightened() and move(); move_to_start() doesn't have to check for "jump"
        # because the shortest path to start never requires going through the sides of the game (aka the gates)
        if self._moving_between_tiles:
            self.__move_between_tiles()
        else:
            check_next_coord, jump = self._calculate_new_coord()

            if self.__coord_dict.get(check_next_coord).is_wall():
                self._direction = self.astar.get_direction(self._coord, self.start_coord)

            if self.__check_neighbours() == True:
                self._direction = self.astar.get_direction(self._coord, self.start_coord)

            if self._coord == self.start_coord:
                self.__movestart = False
                self.set_frightened(False)
                self.__eaten = False
                print(self.__frightened)
                print("stop fightened")
                self.imagechooser()

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
        # the _moving_between_tiles boolean makes the ghost recalculate position to quickly, this function has to slow it down
        # so the ghost doesnt move back and forth without going in a circle
        # this is done by checking if manhattan distance to the target tile is < 1.

        # blinky (red ghost) corner:
        if self.__id == 0:
            self.__target_tile = self.blinky_dict.get(self.__scatter_state)
            if (self.astar.manhattan_distance(self.get_coord().get_coord_tuple(),
                                              self.__target_tile.get_coord_tuple()) < 1):
                self.__scatter_state = (self.__scatter_state + 1) % 4
                print(self.__scatter_state)

        elif self.__id == 1:
            self.__target_tile = self.pinky_dict.get(self.__scatter_state)
            if (self.astar.manhattan_distance(self.get_coord().get_coord_tuple(),
                                              self.__target_tile.get_coord_tuple()) < 1):
                self.__scatter_state = (self.__scatter_state + 1) % 4

        elif self.__id == 2:
            self.__target_tile = self.inky_dict.get(self.__scatter_state)
            if (self.astar.manhattan_distance(self.get_coord().get_coord_tuple(),
                                              self.__target_tile.get_coord_tuple()) < 1):
                self.__scatter_state = (self.__scatter_state + 1) % 3

        elif self.__id == 3:
            self.__target_tile = self.clyde_dict.get(self.__scatter_state)
            if (self.astar.manhattan_distance(self.get_coord().get_coord_tuple(),
                                              self.__target_tile.get_coord_tuple()) < 1):
                self.__scatter_state = (self.__scatter_state + 1) % 3
        return self.__target_tile

    def calculate_direction(self):
        pass  # voor nu

    def __check_neighbours(self):
        horizontal = False
        vertical = False
        x, y = self._coord.get_coord_tuple()
        if (x, y) in Ghost.neighbours_map.keys():
            return Ghost.neighbours_map.get((x, y))
        else:
            keys = self.__coord_dict.keys()
            if (x - 1, y) not in keys or (x + 1, y) not in keys or not self.__coord_dict.get(
                    (x - 1, y)).is_wall() or not self.__coord_dict.get((x + 1, y)).is_wall():
                horizontal = True
            if (x, y + 1) not in keys or (x, y - 1) not in keys or not self.__coord_dict.get(
                    (x, y - 1)).is_wall() or not self.__coord_dict.get((x, y + 1)).is_wall():
                vertical = True
            Ghost.neighbours_map[(x, y)] = horizontal and vertical
        return Ghost.neighbours_map.get((x, y))

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

    def set_eaten(self, value,streak=0):
        self.__eaten = value
        if(self.__eaten):
            scoreimg = str((2**streak)*100) + ".png"
            self.__image = pg.image.load("res/scores/"+scoreimg)
            print(scoreimg)

    def is_frightened(self):
        return self.__frightened


    def is_eaten(self):
        return self.__eaten

    def set_gostart(self, value):
        self.__movestart = value

    def get_gostart(self):
        return self.__movestart
