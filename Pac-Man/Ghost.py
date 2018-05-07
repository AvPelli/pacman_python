import random
from copy import deepcopy

import pygame as pg

from Astar import Astar
from Character import Character
from Coordinate import Coordinate
from Direction import Direction


class Ghost(Character):
    ghost_id = 0
    neighbours_map = {}
    frightened_speed = 1
    image_names = ["blinky", "pinky", "inky", "clyde"]

    def __init__(self, game, coordinate, coord_dict):
        # Start variables
        super().__init__(PIXELSIZE=16, speed=2, moving_pos=0, direction=Direction.UP, game=game, coordinate=coordinate)

        self.__coord_dict = coord_dict
        self.__id = Ghost.ghost_id
        Ghost.ghost_id += 1
        Ghost.ghost_id %= 4
        self._speed = self._normal_speed = (16 - self.__id) / 8.0
        self.astar = Astar(self._game.get_map().get_gates(), self._game.get_pacman())
        self._direction = Direction.UP
        self.imagechooser()
        self.__update_target_tile()

        self.__frightened = False
        self.__frightenedimg = 0
        self.ticks = 0

        self.__eaten = False
        self.__movestart = False
        self.start_time_scatter = pg.time.get_ticks()
        self.__scatter_state = 0
        # blinky scattercoordinates
        self.blinky_dict = {0: Coordinate(21, 5), 1: Coordinate(26, 5), 2: Coordinate(26, 1), 3: Coordinate(21, 1)}
        # pinky scattercoordinates
        self.pinky_dict = {0: Coordinate(6, 5), 1: Coordinate(6, 1), 2: Coordinate(1, 1), 3: Coordinate(1, 5)}
        # inky scattercoordinates
        self.inky_dict = {0: Coordinate(19, 23), 1: Coordinate(26, 29), 2: Coordinate(16, 29)}
        # clyde scattercoordinates
        self.clyde_dict = {0: Coordinate(7, 23), 1: Coordinate(1, 29), 2: Coordinate(12, 29)}
        self.ghost_scatter_coord = [self.blinky_dict, self.pinky_dict, self.inky_dict, self.clyde_dict]

    def imagechooser(self):

        self.__image = pg.image.load("res/ghost/" + Ghost.image_names[self.__id] + "/start.png")

    def start_timer_frightend(self):
        self.start_time_frightened = pg.time.get_ticks()
        self.__frightened = True

    def move_selector(self):
        if self.__frightened and not self.__movestart:
            self._speed = Ghost.frightened_speed
            self.frightened()
            self.frightened_timer = pg.time.get_ticks() - self.start_time_frightened
            frightened_timer_mod = 1 - (250 - self._game.get_candy_amount()) / 500.0
            if (self.frightened_timer > 10000 * frightened_timer_mod):
                self.__frightened = False
                self._game.reset_pacman_streak()
                self.start_time_scatter = pg.time.get_ticks()
                self.imagechooser()
        else:
            self.scatter_timer = pg.time.get_ticks() - self.start_time_scatter
            if self.scatter_timer < 7000:
                self.scatter()
            # Chase 20 seconds
            elif self.scatter_timer < 27000:
                self.move()
            else:
                # Reset timer
                self.start_time_scatter = pg.time.get_ticks()

    def move(self):
        if self._moving_between_tiles:
            self.__move_between_tiles()
        elif self.get_gostart():
            self.move_to_start()
        else:
            check_next_coord, jump = self._calculate_new_coord()
            if self.__coord_dict.get(check_next_coord).is_wall() or self.__check_neighbours():
                self.__update_target_tile()
                if random.random() < 0.90:
                    self._direction = self.astar.get_direction(self._coord,
                                                               self.astar.get_closest_tile(self.__update_target_tile()))
                else:
                    self._direction = self.astar.choose_random(self._coord)

            if jump:
                self._set_on_opposite_side()
            self._moving_between_tiles = True
            # self.check_frightened()
            self._draw_character(self._coord, self.__image)

    def scatter(self):
        if self._moving_between_tiles:
            self.__move_between_tiles()
        elif (self.get_gostart()):
            self.move_to_start()
        else:
            check_next_coord, jump = self._calculate_new_coord()
            self.__update_target_tile_scatter(check_next_coord)
            if self.__coord_dict.get(check_next_coord).is_wall() or self.__check_neighbours():
                path = self.astar.find_path(self._coord, self.__target_tile)
                self._direction = self.astar.dictionary[path[0]]

            if jump:
                self._set_on_opposite_side()
            self._moving_between_tiles = True
            # self.check_frightened()
            self._draw_character(self._coord, self.__image)

    def frightened(self):
        if self._moving_between_tiles:
            self.__move_between_tiles()
        elif (self.get_gostart()):
            self.move_to_start()
        else:
            check_next_coord, jump = self._calculate_new_coord()
            previous_direction = deepcopy(self._direction)
            # frightened mode: random movement
            if self.__coord_dict.get(check_next_coord).is_wall() or self.__check_neighbours():
                self._direction = self.astar.choose_random(self._coord)
                while self._direction is previous_direction.get_reverse() and not jump:
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
            self._direction = self.astar.get_direction(self._coord, self.start_coord)

            self._moving_between_tiles = True
            self.go_eyes()
            self._draw_character(self._coord, self.__image)

            if self._coord == self.start_coord:
                self.reset_character()

    def _draw_character(self, coordinate, image):
        self.check_caught()
        super()._draw_character(coordinate, image)
        self.check_caught()

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
            if self.astar.manhattan_distance(self._coord.get_coord_tuple(), pac_coord.get_coord_tuple()) > 3:
                for i in range(4):
                    pac_coord.update_coord(pac_direction)
            self.__target_tile = pac_coord

        elif self.__id == 2:
            for i in range(2):
                pac_coord.update_coord(pac_direction)
            blinky_coord = (self._game.get_ghosts()[0]).get_coord()
            pac_x, pac_y = pac_coord.get_coord_tuple()
            blinky_x, blinky_y = blinky_coord.get_coord_tuple()
            x_diff, y_diff = pac_x - blinky_x, pac_y - blinky_y
            # aanpassen als move en calculate_direction beter geschreven zijn maar voor nu:

            self.__target_tile = Coordinate(blinky_x + 2 * x_diff, blinky_y + 2 * y_diff)
        else:
            if self.astar.manhattan_distance(pac_coord.get_coord_tuple(), self._coord.get_coord_tuple()) < 10:
                self.__target_tile = Coordinate(pac_coord.get_x() + random.randint(-10, 10),
                                                pac_coord.get_y() + random.randint(-10, 10))
            else:
                self.__target_tile = pac_coord

        self.__target_tile = self.astar.get_closest_tile(self.__target_tile)
        return self.__target_tile

    def __update_target_tile_scatter(self, next_coord):
        # the _moving_between_tiles boolean makes the ghost recalculate position to quickly, this function has to slow it down
        # so the ghost doesnt move back and forth without going in a circle
        # this is done by checking if manhattan distance to the target tile is < 1.
        dictionary = self.ghost_scatter_coord[self.__id]
        self.__target_tile = dictionary.get(self.__scatter_state)
        if (self.astar.manhattan_distance(next_coord,
                                          self.__target_tile.get_coord_tuple()) < 1):
            self.__scatter_state = (self.__scatter_state + 1) % len(dictionary.keys())
        self.__target_tile = self.astar.get_closest_tile(self.__target_tile)
        return self.__target_tile

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

    def check_caught(self):
        if self._coord == self._game.get_pacman_coord() and not self.__movestart:
            if not self.__frightened:
                pg.mixer.Channel(0).stop()
                pg.time.delay(500)
                self._game.set_pacman_caught()
            else:
                if not self.__movestart:
                    self._game.set_ghost_caught()
                    self._game.music_player.play_music("pacman-eatghost/pacman_eatghost.wav")
                    self.set_eaten(True, self._game.get_pacman().get_streak())
                    # Make the ghost start moving to the center
                    self.__movestart = True


    def get_coord(self):
        return self._coord

    def get_normal_speed(self):
        return self._normal_speed

    def set_coord(self, coord):
        self._coord = coord

    def set_frightened(self, value):
        self.__frightened = value

    def set_speed(self, sp):
        self._speed = sp

    def check_frightened(self):
        if self.__frightened:
            self.frightend_image()

    def frightend_image(self):
        self.__image = pg.image.load("res/pacmanghost/bluepacman{number}.png".format(number=self.__frightenedimg % 4))
        self.ticks += 1
        if self.ticks >= 3:
            self.__frightenedimg = self.__frightenedimg + 1
            self.ticks = 0

    def go_eyes(self):
        directionimg = self._direction.get_letter()
        self.__image = pg.image.load("res/eyes/" + directionimg + ".png")
        self._speed = 6

    def reset_character(self):
        super().reset_character()
        self.__movestart = False
        self._speed = self._normal_speed
        self.imagechooser()
        self.set_frightened(False)
        self.__eaten = False
        self._direction = Direction.UP
        self._draw_character(self.start_coord, self.__image)

    def set_eaten(self, value, streak=0):
        self.__eaten = value
        if (self.__eaten):
            score = (2 ** streak) * 100
            scoreimg = str(score) + ".png"
            self._game.get_pacman().add_score(score)
            self.__image = pg.image.load("res/scores/" + scoreimg)
            self._speed = 6
            print(scoreimg)

    def is_frightened(self):
        return self.__frightened

    def is_eaten(self):
        return self.__eaten

    def get_gostart(self):
        return self.__movestart

    def set_frightend_mode(self):
        self.set_speed(Ghost.frightened_speed)
        self.set_frightened(True)
        self.frightened()
