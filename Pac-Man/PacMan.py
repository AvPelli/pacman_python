import random
from copy import deepcopy

import pygame as pg

from Character import Character
from Direction import Direction
from SuperCandy import SuperCandy


class PacMan(Character):
    # Constructor of PacMan
    def __init__(self, game, coordinate, coord_dict, old_score, lifes):
        """
        Initializes Pacman.\n
        Pacman will move through the maze and react to input given (arrow keys) by the user. It will eat the candies\n
        of the Game's Maze object while doing so. The Ghosts will try to prevent this from happening by hunting down\n
        Pacman. When all the candies have been eaten, Pacman wins.\n
        :param game: the game that holds Pacman
        :param coordinate: type: Coordinate: Pacman's starting coordinate
        :param coord_dict: type: {}: represents the whole maze, tells Pacman which coordinates are walls
        :param old_score: type: int
        when a level's finished, a new Pacman will be created and the old ones' score will be given to the new Pacman
        in order to save the current score.\n
        :param lifes: type: int:  similar to old_score, the new Pacman retains the old Pacman's lives
        """
        # Start variables
        super().__init__(PIXELSIZE=16, speed=2, moving_pos=-8,
                         direction=Direction.RIGHT, game=game,
                         coordinate=coordinate)
        self.__score = old_score
        self.__lifes = lifes
        self.__turnaround = False

        # Variables for cosmetics
        self.__number = 1
        self.dict = self.__image_dict()
        self.imageList = self.dict[self._direction.get_letter()]
        self.__image = pg.image.load(
            "res/pacman/pacman-{letter} {number}.png".format(letter=self._direction.get_letter(),
                                                             number=self.__number))

        # Collision and direction control check variables
        self.__coord_dict = coord_dict
        self.__change_direction = None

        self.supercandy_eaten = False
        self.__candies_to_eat = game.get_maze().get_candy_amount()
        self.__streak = 0

    """Draw Methods"""

    def draw_pacman(self):
        """
        Draws Pacman his coordinate.\n
        :return: void
        """
        self._game.get_game_display().blit(self.__image, self._coord.get_pixel_tuple())

    def draw_startpacman(self, coordinate=None):
        """
        When the level has started, this method will draw Pacman between two tiles to appear in the middle.\n
        :param coordinate: optional, the most-right tile to draw Pacman on
        :return: void
        """
        co = coordinate.get_pixel_tuple() if coordinate is not None else self._coord.get_pixel_tuple()
        self._game.get_game_display().blit(self.__image, (co[0] - 8, co[1]))

    """"Move method"""

    def move(self):
        """
        If pacman is moving between tiles, it will keep going that way until it reaches the next tile.\n
        Else this method will check inputs, calculate the coordinate in front of Pacman\n
        and check if Pacman can move this way, then it will assert moving_between_tiles again\n
        :return: void
        """
        if self._moving_between_tiles:
            self.__check_turnaround()
            self.__move_between_tiles()

        # If pacman is not moving, meaning it's on 1 tile exactly, will perform this
        # If Pacman is against a wall it will just redraw itself on the same coordinate, but there are not caluclations needed
        # Else it checks if it needs to calculate a new coordinate, and if a different direction input has been given
        else:
            if not self._movable:
                self._draw_character(self._coord, self.__image)
                return
            # Checks if the direction what was not possible a while ago is possible now
            self.__direction_waiter()
            # Calculates the next coordinate
            check_next_coord, jump = self._calculate_new_coord()

            # Checks if the new coordinate is a wall
            # If it is a wall, it will not move ( as long as the direction isn't changed)
            # Else it can start moving there in the next iteration (will perform if self.__moving_between_tiles:)

            self._moving_between_tiles = True

            if jump:
                self._set_on_opposite_side()
            elif self.__coord_dict.get(check_next_coord).is_wall():
                self.__moveable = False
                self._moving_between_tiles = False

            self._draw_character(self._coord, self.__image)
            # Moves to the new coordinate
            # Checks if there is candy to eat on the new coordinate
            self.__eat_fruit()

    def __move_between_tiles(self):
        """
        This method is used whenever Pacman's moving between 2 tiles in order to make a smooth transition\n
        from one coordinate to another. When Pacman has reached the next tile, it will update its coordinate\n
        and will set moving_between_tiles to false, in order for the move method to check inputs and whatnot.\n
        :return: void
        """
        if not self.__turnaround:
            # Proceed to the next tile
            self.__image = self.__get_image_direction(self._direction)
            super()._move_between_tiles()
            if 10 <= self._moving_pos <= 13:
                self.__eat_candy()
        # However if turnaround has been set (see check_turnaround), pacman will have to move back to the beginning his original tile 1st
        # Once there he'll set himself ready for the next iteration (and its coordinate will NOT be updated)
        # To solve issues bug-wise, number will be set on 0 once it has moved back, so its beak is closed at the end, as usual
        # Also note that, while the image will be reversed, pacman's direction will not be updated until he has finished moving so prevent extra issues that cause all sorts of headaches
        else:
            self.__image = self.__get_image_direction(self.__change_direction)
            self._moving_pos -= self._speed
            if self._moving_pos <= 0:
                self._moving_pos = 0
                self._moving_between_tiles = False
                self.__turnaround = False
                self.__number = 0

        self._draw_character(self._coord, self.__image)

    # This method will change the direction to the change_direction variable if it is possible
    # So when someone has pressed UP-key and it was not possible at that moment, this method will change the direction to UP
    # As soon as it is possible, therefor we check if pacmans its coordinates  added with the direction it would be change to is not a wall
    # If so it will change the moving direction
    def __direction_waiter(self):
        """
        Sets Pacman's direction, this will bind a previously given (overridable) input to Pacman's actual direction\n
        whenever it has the chance to, this is to prevent having to give in inputs at the perfect moment.\n
        :return: void
        """
        if not self._moving_between_tiles and self.__change_direction is not None:
            x, y = self._coord.get_x() + self.__change_direction.value[0], self._coord.get_y() + \
                   self.__change_direction.value[1]
            if (x, y) in self.__coord_dict.keys() and not self.__coord_dict.get((x, y)).is_wall():
                self._direction = self.__change_direction

    """Eat Methods"""

    # Checks if there is a candy object on Pacmans coordinate
    # If so it will delete that Candy object out of the dictionary (So it will not be redrawn)
    def __eat_candy(self):
        """
        Gets the candy positions from the Maze and checks if Pacman's currently on top of one.\n
        If so, Pacman will eat the candy and that candy will be removed from the Maze's list.\n
        :return: void
        """
        candies = self._game.get_maze().get_candy_dict()
        self.__candies_to_eat = len(candies)
        next_coord = deepcopy(self._coord)
        next_coord.update_coord(self._direction)
        if next_coord in candies.keys():
            candy = candies[next_coord]
            if isinstance(candy, SuperCandy):
                self.supercandy_eaten = True
            self.__score += candy.get_score()
            self._game.update_fruit_selector()
            pg.mixer.Channel(1).play(pg.mixer.Sound("res/files/music/pacman-chomp/pacman-wakawaka.wav"))
            del self._game.get_maze().get_candy_dict()[next_coord]

    def __eat_fruit(self):
        """
        Checks firstly if Pacman's on the Fruit coordinate, where Fruits will spawn, then it will check.\n
        if a fruit's currently active. If it is, Pacman will eat the fruit.\n
        :return: void
        """
        coordtuple = self._coord.get_x(), self._coord.get_y()
        fruit_coordt = self._game.get_fruit_selector().get_fruit_coord_tuple()
        if (coordtuple[0] == fruit_coordt[0] or coordtuple[0] == fruit_coordt[0] + 1) and coordtuple[1] == fruit_coordt[
            1]:
            selector = self._game.get_fruit_selector()
            if selector.fruit_active():
                pg.mixer.Channel(1).play(pg.mixer.Sound("res/files/music/pacman-eatfruit/pacman_eatfruit.wav"))
                self.add_score(selector.get_score())

    """Hulp Methods"""

    def __check_turnaround(self):
        """
        When pacman is moving between tiles, he should still be able to immediately turn around instead of\n
        moving to the next tile first. This method will check if an opposite key has\n
        been pressed and sets the variable __turnaround.\n
        :return: void
        """
        if self.__change_direction is not None:
            x_direction = self._direction.value[0] + self.__change_direction.value[0]
            y_direction = self._direction.value[1] + self.__change_direction.value[1]
            self.__turnaround = x_direction == 0 and y_direction == 0

    def add_score(self, value):
        """
        Adds the given param to Pacman's current score, this method is usually called whenever Pacman eats an Object.\n
        :param value: int
        :return: void
        """
        self.__score += value

    def decrease_lifes(self):
        """
        When Pacman is eaten, this method will decrease Pacman's lives and, if zero, force game over
        Otherwise you can try again to get a higher score
        :return: void
        """
        self.__lifes -= 1
        self._game.set_lifes(self.__lifes)
        if self.__lifes <= 0:
            self._game.set_gamemode(5)
        else:
            self._game.set_gamemode(4)
            self._game.music_player.stop_background_music()
            pg.time.delay(1000)
            self._game.music_player.play_music("pacman-death/pacman_death.wav")
            self._game.draw_pacman_death(self._coord)

    """"Getters"""

    def is_super_candy_eaten(self):
        """
        Returns whether or not a SuperCandy has been eaten, which is used to force the Ghosts into frightened mode.\n
        :return: boolean
        """
        return self.supercandy_eaten

    def get_lifes(self):
        """
        Returns Pacman's current lifes left.\n
        :return: int
        """
        return self.__lifes

    def get_score(self):
        """
        Returns Pacman's score.\n
        :return: int
        """
        return self.__score

    def get_coord(self):
        """
        Returns a copy of Pacman's coordinate.\n
        :return: Coordinate
        """
        # Deepcopy for elimination of privacy leak
        return deepcopy(self._coord)

    def get_streak(self):
        """
        Returns the current ghost-eating streak, that resets when the Ghosts' frightened timer runs out.\n
        :return: int
        """
        return self.__streak

    def __get_image_direction(self, direction):
        """
        Returns the current loaded image for Pacman, utilizing its image dictionary, and the current direction of Pacman
        :param direction: direction that Pacman is facing
        :return: image
        """
        self.__number = (self.__number + 1) % 8
        return pg.image.load(
            self.dict[direction.get_letter()][self.__number]) if direction is not None else pg.image.load(
            "res/pacmandeath/1.png")

    def get_candies_to_eat(self):
        """
        Returns the amount of candies left on the map for Pacman to eat
        :return: int
        """
        return self.__candies_to_eat

    """"Setters"""

    # Setter: this method sets the given direction
    # If the following coordinate (if you follows the given direction) is a wall
    # It will put the given direction in the change_direction variable (More info in __direction_changer method)
    def set_direction(self, direction):
        """
        This method will try binding the current input to Pacman's direction, when Pacman's able to\n
        move in that direction. Otherwise the input is stored into change_direction (see direction_waiter).\n
        :param direction: (future) direction Pacman will face
        :return: void
        """
        x, y = self._coord.get_x() + direction.x, self._coord.get_y() + direction.y
        if (x, y) not in self.__coord_dict.keys() or self.__coord_dict.get((x, y)).is_wall():
            self.__change_direction = direction
            return
        if self._moving_between_tiles:
            self.__change_direction = direction
        else:
            self.__change_direction = None
            self._direction = direction
            self._moveable = True

    def set_streak(self):
        """
        Adds 1 to the current ghost-eating streak to increase the score given from eating frightened ghosts.\n
        :return: void
        """
        self.__streak += 1

    """"Initialize methods """

    # Initialize the image dictionary
    def __image_dict(self):
        """
        Creates and returns an image dictionary for Pacman, containing all it's frame pictures and in
        every direction possible
        :return: image dictionary
        """
        dict = {}
        for letter in "ldru":
            dict[letter] = list()
            for i in range(1, 10):
                dict[letter].append("res/pacman/pacman-{letter} {number}.png".format(letter=letter, number=i))
        return dict

    """"Reset Methods"""""

    # Does move Pac-Man to original start coordinate and sets the direction  LEFT
    def reset_character(self):
        """
        Resets Pacman, this uses the basic functions from the method in Character, also also resets the Direction
        :return: void
        """
        super().reset_character()
        self._direction = [Direction.LEFT, Direction.RIGHT][random.randint(0, 1)]
        self.__change_direction = None

    def reset_streak(self):
        """
        Resets Pacman's current ghost-eating streak, this method is called when the frightened\n
        timer of the ghosts runs out.\n
        :return: void
        """
        self.__streak = 0
