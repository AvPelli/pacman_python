import math
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
        """
        Creates Ghost object.\n
        Each ghost has a unique id, boolean values for each state (frightened/eaten/scatter),
        its own pathfinder (Astar algorithm) and scatter coordinates.
        :param game: The game object that runs the Ghost
        :param coordinate: The startcoordinate of the Ghost
        :param coord_dict: Dictionary that maps tuple -> Coordinate, this dictionary contains information about walls
        :return: void
        """
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

        self.__extreme_mode = False

        self.__eaten = False
        self.__movestart = False
        self.start_time_scatter = 0
        self.__scatter_state = None
        # blinky scattercoordinates
        self.blinky_dict = {0: Coordinate(21, 5), 1: Coordinate(26, 5), 2: Coordinate(26, 1), 3: Coordinate(21, 1)}
        # pinky scattercoordinates
        self.pinky_dict = {0: Coordinate(6, 5), 1: Coordinate(6, 1), 2: Coordinate(1, 1), 3: Coordinate(1, 5)}
        # inky scattercoordinates
        self.inky_dict = {0: Coordinate(21, 23), 1: Coordinate(26, 28), 2: Coordinate(21, 29), 3: Coordinate(15, 29)}
        # clyde scattercoordinates
        self.clyde_dict = {0: Coordinate(6, 23), 1: Coordinate(1, 29), 2: Coordinate(6, 29), 3: Coordinate(12, 29)}
        self.ghost_scatter_coord = [self.blinky_dict, self.pinky_dict, self.inky_dict, self.clyde_dict]

    def imagechooser(self):
        """
        Chooses the appropriate image for each ghost, based on the ghost's id
        :return: void
        """
        self.__image = pg.image.load("res/ghost/" + Ghost.image_names[self.__id] + "/start.png")

    def start_timer_frightend(self):
        """
        Starts the timer for frightened mode by saving current gametime and checking time difference later on
        :return: void
        """
        self.start_time_frightened = pg.time.get_ticks()
        self.__frightenedimg = 0
        self.__frightened = True

    def move_selector(self):
        """
        Handles how the Ghost moves, this is different for each state (Scatter,Frightened,Eaten)\n
        This method uses the timers for each state to switch between states.
        :return: void
        """
        if self.__movestart:
            self.move_to_start()
        elif self.__frightened:
            self._speed = Ghost.frightened_speed
            self.frightened_timer = pg.time.get_ticks() - self.start_time_frightened
            self.frightened_timer_mod = (1 - (250 - self._game.get_candy_amount()) / 500.0) * 10000
            self.frightened()
            if (self.frightened_timer > self.frightened_timer_mod):
                self.__frightened = False
                self._speed = self._normal_speed
                self.start_time_scatter = pg.time.get_ticks()
                self.imagechooser()
        elif not self.__extreme_mode:
            self.scatter_timer = pg.time.get_ticks() - self.start_time_scatter
            # print(Ghost.image_names[self.__id]  + str(self.scatter_timer))
            if self.scatter_timer < 7000:
                self.check_scatter_state()
                self.scatter()
            # Chase 20 seconds
            elif self.scatter_timer < 27000:
                self.__scatter_state = None
                self.move()
            else:
                # Reset timer
                self.start_time_scatter = pg.time.get_ticks()
        else:
            self.move()

    def move(self):
        """
        Handles how the Ghost moves in its normal state\n
        In extreme mode the Ghosts can move direction at any time, instead of only switching directions at intersections
        :return: void
        """
        if self._moving_between_tiles:
            self.__move_between_tiles()
        else:
            check_next_coord, jump = self._calculate_new_coord()
            if (self.__coord_dict.get(
                    check_next_coord).is_wall() or self.__check_neighbours()) and not self.__extreme_mode:
                self.__update_target_tile()
                self._direction = self.astar.get_direction(self._coord,
                                                           self.astar.get_closest_tile(self.__update_target_tile()))
            elif self.__extreme_mode:
                self.__update_target_tile()
                self._direction = self.astar.get_direction(self._coord,
                                                           self.astar.get_closest_tile(self.__update_target_tile()))
            if jump:
                self._set_on_opposite_side()
            self._moving_between_tiles = True
            self._draw_character(self._coord, self.__image)

    def scatter(self):
        """
        Handles how the Ghost moves in scatter state \n
        Each Ghost loops through its respective scatter coordinates which form a circle in a specific corner of the Maze
        :return: void
        """
        if self._moving_between_tiles:
            self.__move_between_tiles()
        else:
            check_next_coord, jump = self._calculate_new_coord()
            self.__update_target_tile_scatter(check_next_coord)
            if self.__coord_dict.get(check_next_coord).is_wall() or self.__check_neighbours():
                path = self.astar.find_path(self._coord, self.__target_tile)
                self._direction = self.astar.dictionary[path[0]]
            if jump:
                self._set_on_opposite_side()
            self._moving_between_tiles = True
            self._draw_character(self._coord, self.__image)

    def frightened(self):
        """
        Handles how the Ghost moves in frightened state \n
        In this state Ghost's speed is decreased and moves randomly
        :return: void
        """
        if self._moving_between_tiles:
            self.__move_between_tiles()
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
        """
        Handles Ghost movement to starting position, for example after being eaten\n
        Note: Unlike scatter(), frightened() and move(); move_to_start() doesn't have to check for "jump"
        because the shortest path to start never requires going through the sides of the game (aka the gates)
        :return: void
        """
        if self._moving_between_tiles:
            self.__move_between_tiles()
        else:
            self._direction = self.astar.get_direction(self._coord, self.start_coord)

            self._moving_between_tiles = True
            self.display_eyes_score()
            self._draw_character(self._coord, self.__image)

            if self._coord == self.start_coord:
                self.reset_character()

    def _draw_character(self, coordinate, image):
        """
        Ghost gets drawn on coordinate, the image is dependent on the state of the Ghost
        :param coordinate: Coordinate where Ghost should be drawn
        :param image: Visual display of the Ghost
        :return: void
        """
        self.check_caught()
        super()._draw_character(coordinate, image)
        self.check_caught()

    def __move_between_tiles(self):
        """
        Proceed to the next tile.
        Handles movement between 2 tiles, this takes into account the Ghost's speed.
        :return: void
        """
        super()._move_between_tiles()
        self._draw_character(self._coord, self.__image)

    def __update_target_tile(self):
        """
        Implements the Ghost's chase behaviour:
        based on the Ghost's id, a different tile gets chosen as new target tile
        :return: void
        """
        pac_coord = self._game.get_pacman_coord()
        pac_direction = self._game.get_pacman_direction()
        if self.__id == 0:
            self.__target_tile = pac_coord
            return self.__target_tile
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
            distance = self.astar.manhattan_distance(pac_coord.get_coord_tuple(), self._coord.get_coord_tuple())
            if distance < 10 and distance > 2:
                self.__target_tile = Coordinate(pac_coord.get_x() + random.randint(-10, 10),
                                                pac_coord.get_y() + random.randint(-10, 10))
            else:
                self.__target_tile = pac_coord

        self.__target_tile = self.astar.get_closest_tile(self.__target_tile)
        return self.__target_tile

    def __update_target_tile_scatter(self, next_coord):
        """
        The _moving_between_tiles boolean makes the ghost recalculate position to quickly, this function has to slow it down
        so the ghost doesnt move back and forth without going in a circle
        this is done by checking if manhattan distance to the target tile is < 1.
        :return: void
        """
        dictionary = self.ghost_scatter_coord[self.__id]
        self.__target_tile = dictionary.get(self.__scatter_state)
        if (self.astar.manhattan_distance(next_coord,
                                          self.__target_tile.get_coord_tuple()) < 1):
            self.__scatter_state = (self.__scatter_state + 1) % len(dictionary.keys())
        self.__target_tile = self.astar.get_closest_tile(self.__target_tile)
        return self.__target_tile

    def __check_neighbours(self):
        """
        Checks the surrounding tiles to see if there are any walls and returns their coordinates.
        :return: tuple (int,int)
        """
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
        """
        Checks if the Ghost is caught, which means that pacman's coordinate is the same as the Ghost's.
        :return: void
        """
        if self._coord == self._game.get_pacman_coord() and not self.__movestart:
            if not self.__frightened:
                pg.mixer.Channel(0).stop()
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

    def set_extreme(self, bool):
        self.__extreme_mode = bool

    def check_frightened(self):
        if self.__frightened:
            self.frightend_image()

    def init_start_scatter(self):
        self.start_time_scatter = pg.time.get_ticks()

    def frightend_image(self):
        self.__image = pg.image.load("res/pacmanghost/bluepacman{number}.png".format(number=self.__frightenedimg % 4))
        time_remaining = self.frightened_timer_mod - self.frightened_timer
        if time_remaining < self.frightened_timer_mod / 2:
            self.ticks += 1
            waarde = 2 if time_remaining < self.frightened_timer_mod / 2 and time_remaining > self.frightened_timer_mod / 4 else 1
            if self.ticks >= waarde:
                self.__frightenedimg = self.__frightenedimg + 1
                self.ticks = 0
        else:
            self.__frightenedimg = self.__frightenedimg + 2

    def display_eyes_score(self):
        time_score = pg.time.get_ticks() - self.__score_time
        if time_score > 380:
            directionimg = self._direction.get_letter()
            self.__image = pg.image.load("res/eyes/" + directionimg + ".png")
            self._speed = 6

    def reset_character(self):
        """
        Resets the Ghost to default values and start coordinate
        :return: void
        """
        super().reset_character()
        self.__movestart = False
        self._speed = self._normal_speed
        self.imagechooser()
        self.set_frightened(False)
        self.__frightenedimg = 0
        self.__eaten = False
        self._direction = Direction.UP
        self._draw_character(self.start_coord, self.__image)

    def set_eaten(self, value, streak=0):
        """
        Set Ghost to eaten state
        :param value:
        :param streak: The streak defines how many points are awarded for eating the Ghost
        :return: void
        """
        self.__eaten = value
        if (self.__eaten):
            score = (2 ** streak) * 100
            scoreimg = str(score) + ".png"
            self._game.get_pacman().add_score(score)
            self.__image = pg.image.load("res/scores/" + scoreimg)
            self.__score_time = pg.time.get_ticks()
            self._speed = 6
            print(scoreimg)

    def is_frightened(self):
        """
        Returns True if Ghost is frightened
        :return: boolean
        """
        return self.__frightened

    def is_eaten(self):
        """
        Returns True if Ghost is eaten
        :return: boolean
        """
        return self.__eaten

    def get_movestart(self):
        """
        Returns True if the Ghost has to move back to start position
        :return: boolean
        """
        return self.__movestart

    def check_scatter_state(self):
        """
        Handles which coordinate in the scatter dictionary the Ghost will move to first
        :return: void
        """
        if self.__scatter_state is not None:
            return
        best_option = -1
        closest_coord = math.inf
        dict = self.ghost_scatter_coord[self.__id]
        for state, coord in dict.items():
            distance = self.astar.manhattan_distance(self._coord.get_coord_tuple(), coord.get_coord_tuple())
            if (distance < closest_coord):
                closest_coord = distance
                best_option = state
        self.__scatter_state = best_option
