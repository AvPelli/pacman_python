import random
from copy import deepcopy

import math
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
        Each ghost has a unique id, boolean values for each state (frightened/eaten/scatter),\n
        its own pathfinder (Astar algorithm) and scatter coordinates.\n
        :param game: The game object that runs the Ghost
        :param coordinate: The startcoordinate of the Ghost
        :param coord_dict: Dictionary that maps tuple -> Coordinate, this dictionary contains information about walls
        """
        # Start variables
        super().__init__(PIXELSIZE=16, speed=2, moving_pos=0, direction=Direction.UP, game=game, coordinate=coordinate)

        self.__coord_dict = coord_dict
        self.__id = Ghost.ghost_id
        Ghost.ghost_id += 1
        Ghost.ghost_id %= 4
        self._speedfactor = (self._game.get_won_counter() * 0.11) + 1
        self._speed = self._normal_speed = ((16 - self.__id) / 8.0) * self._speedfactor
        self.astar = Astar(self._game.get_maze().get_gates())
        self._direction = Direction.UP
        self.image_chooser()
        self.__update_target_tile()

        self.__frightened = False
        self.__frightenedimg = 0
        self.ticks = 0

        self.__extreme_mode = False

        self.__eaten = False
        self.__movestart = False
        self.start_time_scatter = 0
        self.__scatter_state = None
        # blinky scatter coordinates
        self.blinky_dict = {0: Coordinate(21, 5), 1: Coordinate(26, 5), 2: Coordinate(26, 1), 3: Coordinate(21, 1)}
        # pinky scatter coordinates
        self.pinky_dict = {0: Coordinate(6, 5), 1: Coordinate(6, 1), 2: Coordinate(1, 1), 3: Coordinate(1, 5)}
        # inky scatter coordinates
        self.inky_dict = {0: Coordinate(21, 23), 1: Coordinate(26, 28), 2: Coordinate(21, 29), 3: Coordinate(15, 29)}
        # clyde scatter coordinates
        self.clyde_dict = {0: Coordinate(6, 23), 1: Coordinate(1, 29), 2: Coordinate(6, 29), 3: Coordinate(12, 29)}
        self.ghost_scatter_coord = [self.blinky_dict, self.pinky_dict, self.inky_dict, self.clyde_dict]

    """Image chooser Methods"""

    def image_chooser(self):
        """
        Chooses the appropriate image for each ghost, based on the ghost's id.\n
        :return: void
        """
        self.__image = pg.image.load("res/ghost/" + Ghost.image_names[self.__id] + "/start.png")

    def frightend_image(self):
        """
        When Pacman has eaten a SuperCandy, the ghosts have to update their current image to its frightened version.\n
        When the frightened timer is almost over, the image will be switch between a blue and a white frightened variant.\n
        :return: void
        """
        self.__image = pg.image.load("res/pacmanghost/bluepacman{number}.png".format(number=self.__frightenedimg % 4))
        time_remaining = self.frightened_timer_mod - self.frightened_timer
        if time_remaining < self.frightened_timer_mod / 2:
            self.ticks += 1
            value = 2 if (self.frightened_timer_mod / 2) > time_remaining > (self.frightened_timer_mod / 4) else 1
            if self.ticks >= value:
                self.__frightenedimg = self.__frightenedimg + 1
                self.ticks = 0
        else:
            self.__frightenedimg = self.__frightenedimg + 2

    def display_eyes_score(self):
        """
        When the Ghost is eaten, this method will set its new current image that has to be shown; the eyes.\n
        :return: void
        """
        time_score = pg.time.get_ticks() - self.__score_time
        if time_score > 580:
            directionimg = self._direction.get_letter()
            self.__image = pg.image.load("res/eyes/" + directionimg + ".png")
            self._speed = 6

    """Move Methods"""

    def move_selector(self):
        """
        Handles how the Ghost moves, this is different for each state (Scatter,Frightened,Eaten/Chase)\n
        This method uses the timers for each state to switch between states.\n
        In extreme mode the ghosts can only perform Chase and Frightened mode.\n
        :return: void
        """
        if self.__movestart:
            self.move_to_start()
        elif self.__frightened:
            self._speed = Ghost.frightened_speed
            self.frightened_timer = pg.time.get_ticks() - self.start_time_frightened
            self.frightened_timer_mod = (1 - (250 - self._game.get_candy_amount()) / 500.0) * 10000
            self.frightened()
            if self.frightened_timer > self.frightened_timer_mod:
                self.__frightened = False
                self._speed = self._normal_speed
                self.start_time_scatter = pg.time.get_ticks()
                self.image_chooser()
        elif not self.__extreme_mode:
            self.scatter_timer = pg.time.get_ticks() - self.start_time_scatter
            # Scatter 7 seconds
            if self.scatter_timer < 7000:
                # Looks which scatter coordinate is the closest one
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
        In extreme mode the Ghosts can move direction at any time, instead of only switching directions at intersections or turns.\n
        :return: void
        """
        if self._moving_between_tiles:
            self.__move_between_tiles()
        else:
            check_next_coord, jump = self._calculate_new_coord()
            # Checks if the next calculated coordinate is a wall or if there is an intersection/turn (and extreme mode deactivated)
            # If so it wil calculate a new direction. This is so for most of the following moving methods (scatter/frightened)
            if (self.__coord_dict.get(
                    check_next_coord).is_wall() or self.__check_neighbours()) and not self.__extreme_mode:
                self.__update_target_tile()
                self._direction = self.astar.get_direction(self._coord,
                                                           self.astar.get_closest_tile(self.__update_target_tile()))
            elif self.__extreme_mode:
                # Calculates immediately a new direction
                self.__update_target_tile()
                self._direction = self.astar.get_direction(self._coord,
                                                           self.astar.get_closest_tile(self.__update_target_tile()))
            # Looks if the ghosts need to perform a set on opposite side movement
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
        In this state Ghost's speed is decreased and moves randomly.\n
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
        Note: Unlike scatter(), frightened() and move(); move_to_start() doesn't have to check for "jump"\n
        because the shortest path to start never requires going through the sides of the game (aka the gates).\n
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

    def __move_between_tiles(self):
        """
        Proceed onwards to the next tile.\n
        Handles movement between 2 tiles, this takes the Ghost's speed into account.\n
        :return: void
        """
        super()._move_between_tiles()
        self._draw_character(self._coord, self.__image)

    """Draw Method"""

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

    """Update target tile Methods"""

    def __update_target_tile(self):
        """
        Implements the Ghost's chase behaviour:\n
        based on the Ghost's id, a different tile gets chosen as new target tile. The Ghost will then try to reach this tile\n
        Ghost -->   Target tile\n
        Blinky -->  Pacman's tile\n
        Pinky -->   If possible 4 tiles ahead of Pacman in his moving direction\n
        Inky -->    It calculates a vector with information of Blinky and Pacman. It goes to the end of the vector\n
        Clyde -->   If his distance from pacman is > 10  or < 2 his target tile is pacman's tile,\n
                    otherwise it is a random number from -10 --> +10 added to both x en y value of pacman's coordinate\n
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
            self.__target_tile = Coordinate(blinky_x + 2 * x_diff, blinky_y + 2 * y_diff)
        else:
            distance = self.astar.manhattan_distance(pac_coord.get_coord_tuple(), self._coord.get_coord_tuple())
            if 10 > distance > 2:
                self.__target_tile = Coordinate(pac_coord.get_x() + random.randint(-10, 10),
                                                pac_coord.get_y() + random.randint(-10, 10))
            else:
                self.__target_tile = pac_coord

        self.__target_tile = self.astar.get_closest_tile(self.__target_tile)
        return self.__target_tile

    def __update_target_tile_scatter(self, next_coord):
        """
        The _moving_between_tiles boolean makes the ghost recalculate position to quickly, this function has to slow it down\n
        so the ghost doesnt move back and forth without going in a circle\n
        this is done by checking if manhattan distance to the target tile is < 1.\n
        :return: void
        """
        dictionary = self.ghost_scatter_coord[self.__id]
        self.__target_tile = dictionary.get(self.__scatter_state)
        if (self.astar.manhattan_distance(next_coord,
                                          self.__target_tile.get_coord_tuple()) < 1):
            self.__scatter_state = (self.__scatter_state + 1) % len(dictionary.keys())
        self.__target_tile = self.astar.get_closest_tile(self.__target_tile)
        return self.__target_tile

    """Check Methods"""

    def __check_neighbours(self):
        """
        Checks the surrounding tiles to see if there are any walls and returns their coordinates.\n
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
        Checks if the Ghost is caught, which means that Pacman's coordinate is the same as the Ghost's.\n
        :return: void
        """
        if self._coord == self._game.get_pacman_coord() and not self.__movestart:
            if not self.__frightened:
                self._game.set_pacman_caught()
            else:
                if not self.__movestart:
                    self._game.set_ghost_caught()
                    self._game.music_player.play_music("pacman-eatghost/pacman_eatghost.wav")
                    self.set_eaten(True, self._game.get_pacman().get_streak())
                    # Make the ghost start moving to the center
                    self.__movestart = True

    def check_frightened(self):
        """
        If the ghost is frightened, it has to show a different image instead.\n
        This method uses frightened_image to set its current image.\n
        :return: void
        """
        if self.__frightened:
            self.frightend_image()

    def check_scatter_state(self):
        """
        Handles which coordinate in the scatter dictionary the Ghost will move to first\n
        It will always go to the closest scatter coordinate possible.\n
        :return: void
        """
        if self.__scatter_state is not None:
            return
        best_option = -1
        closest_coord = math.inf
        scatter_dict = self.ghost_scatter_coord[self.__id]
        for state, coord in scatter_dict.items():
            distance = self.astar.manhattan_distance(self._coord.get_coord_tuple(), coord.get_coord_tuple())
            if distance < closest_coord:
                closest_coord = distance
                best_option = state
        self.__scatter_state = best_option

    """Hulp/Start timer Methods"""

    def init_start_scatter(self):
        """
        Initializes the scatter timer by setting it's start_timer_scatter variable to the current time.\n
        :return: void
        """
        self.start_time_scatter = pg.time.get_ticks()

    def start_timer_frightend(self):
        """
        Starts the timer for frightened mode by saving current gametime and checking time difference later on.\n
        :return: void
        """
        self.start_time_frightened = pg.time.get_ticks()
        self.__frightenedimg = 0
        self.__frightened = True

    def reset_character(self):
        """
        Resets the Ghost to default values and start coordinate, called when the level has finished.\n
        :return: void
        """
        super().reset_character()
        self.__movestart = False
        self._speed = self._normal_speed
        self.image_chooser()
        self.set_frightened(False)
        self.__frightenedimg = 0
        self.__eaten = False
        self._direction = Direction.UP
        self._draw_character(self.start_coord, self.__image)

    """Getters"""

    def is_frightened(self):
        """
        Returns True if Ghost is currently frightened.\n
        :return: boolean
        """
        return self.__frightened

    def is_eaten(self):
        """
        Returns True if Ghost is eaten by Pacman.\n
        :return: boolean
        """
        return self.__eaten

    def get_movestart(self):
        """
        Returns True if the Ghost has to move back to start position.\n
        :return: boolean
        """
        return self.__movestart

    def get_normal_speed(self):
        """
        Getter, returns the ghost's normal speed; the speed when it is neither frightened nor eaten by Pacman.\n
        :return: double
        """
        return self._normal_speed

    """Setters"""

    def set_frightened(self, value):
        """
        Sets the ghost in frightened mode; when Pacman has eaten a SuperCandy.\n
        :param value: type: boolean
        :return: void
        """
        self.__frightened = value

    def set_speed(self, speed):
        """
        Sets the Ghost's actual speed, called when Pacman has eaten a SuperCandy, when the frightened timer has run out,\n
        when Pacman has eaten the ghost,...\n
        :param speed: type: double
        :return: void
        """
        self._speed = speed

    def set_extreme(self, boolean):
        """
        A hidden feature within the game.\n
        Sets whether or not the ghosts should become way smarter and more efficient at hunting Pacman down.\n
        Activated by pressing 'E' in the start of the game.\n
        :param boolean: boolean
        :return: void
        """
        self.__extreme_mode = boolean

    def set_eaten(self, value, streak=0):
        """
        Sets the Ghost to the eaten state, meaning Pacman has just eaten it and awards score to Pacman.\n
        :param value: Whether or not Ghost has been eaten
        :param streak:  Defines how many points are awarded for eating the Ghost
        :return: void
        """
        self.__eaten = value
        if self.__eaten:
            score = (2 ** streak) * 100
            scoreimg = str(score) + ".png"
            self._game.get_pacman().add_score(score)
            self.__image = pg.image.load("res/scores/" + scoreimg)
            self.__score_time = pg.time.get_ticks()
            self._speed = 6
