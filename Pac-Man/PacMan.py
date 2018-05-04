import pygame as pg

from Character import Character
from Direction import Direction
from SuperCandy import SuperCandy


class PacMan(Character):
    # Constructor of PacMan
    def __init__(self, game, coordinate, coord_dict):
        # Start variables
        super().__init__(PIXELSIZE=16, speed=2, moving_pos=-8,
                         direction=Direction.RIGHT, game=game,
                         coordinate=coordinate)
        self.score = 0
        self.lifes = 4
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
        self.__streak = 0

    # draw pacman on that coordinate
    def draw_pacman(self):
        self._game.get_game_display().blit(self.__image, self._coord.get_pixel_tuple())

    # Initializes Pacman on give start coordinate
    def draw_startpacman(self, coordinate):
        co = coordinate.get_pixel_tuple()
        self._game.get_game_display().blit(self.__image, (co[0] - 8, co[1]))

    """"Move method"""

    # The move method will move Pacman
    def move(self):
        # If pacman is moving between tiles, it will keep going that way until it reaches the next tile
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
            self.__eat_candy()

    # Function that is used while pacman is moving form one coordinate to another
    def __move_between_tiles(self):
        if not self.__turnaround:
            # Proceed to the next tile
            self.__image = self.__get_image_direction(self._direction)
            super()._move_between_tiles()
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
        if not self._moving_between_tiles and self.__change_direction is not None:
            x, y = self._coord.get_x() + self.__change_direction.value[0], self._coord.get_y() + \
                   self.__change_direction.value[1]
            if (x, y) in self.__coord_dict.keys() and not self.__coord_dict.get((x, y)).is_wall():
                self._direction = self.__change_direction

    # Checks if there is a candy object on Pacmans coordinate
    # If so it will delete that Candy object out of the dictionary (So it will not be redrawn)
    # Also the first time this method gets used it will load the music of eating fruit
    def __eat_candy(self):
        candies = self._game.get_map().get_candy_dict()
        if self._coord in candies.keys():
            candy = candies[self._coord]
            if isinstance(candy, SuperCandy):
                self.supercandy_eaten = True
            self.score += candy.get_score()
            pg.mixer.Channel(1).play(pg.mixer.Sound("res/files/music/pacman-chomp/pacman-wakawaka.wav"))
            del self._game.get_map().get_candy_dict()[self._coord]

    # When pacman is moving between tiles, he should still be able to immediately turn around instead of finishing moving to the next tile 1st,
    # This method will check if an opposite key has been pressed and sets the variable __turnaround
    def __check_turnaround(self):
        if self.__change_direction is not None:
            x_direction = self._direction.value[0] + self.__change_direction.value[0]
            y_direction = self._direction.value[1] + self.__change_direction.value[1]
            self.__turnaround = x_direction == 0 and y_direction == 0
        return None

    """"Getters"""

    def is_super_candy_eaten(self):
        return self.supercandy_eaten

    # Returns the amount of lifes left
    def get_lifes(self):
        return self.lifes

    # Returns the score
    def get_score(self):
        return self.score

    # Return
    def get_coord(self):
        return self._coord

    def get_streak(self):
        return self.__streak

    """"Setters"""

    # Setter: this method sets the given direction
    # If the following coorinate (if you follows the given direction) is a wall
    # It will put the given direction in the change_direction variable (More info in __direction_changer methode)
    def set_direction(self, direction):
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

    # Setter for pacman lifes, to access the pacmanlifes in the Game class
    def set_lifes(self, lifes):
        self.lifes = lifes

    def set_coord(self, coordinate):
        self._coord = coordinate

    def set_streak(self, eatstreak):
        self.__streak = self.__streak + eatstreak

    def reset_streak(self):
        self.__streak = 0

    """"Getters"""

    # Getter: Returns the image if needs to use for the give direction (And animation)
    def __get_image_direction(self, direction):
        self.__number = (self.__number + 1) % 8
        return pg.image.load(self.dict[direction.get_letter()][self.__number])

    """"Initialize methods """

    # Initialize the image dictionary
    def __image_dict(self):
        dict = {}
        for letter in "ldru":
            dict[letter] = list()
            for i in range(1, 10):
                dict[letter].append("res/pacman/pacman-{letter} {number}.png".format(letter=letter, number=i))
        return dict

    """"Reset Method"""""

    # Does move Pac-Man to original start coordinate and sets the direction  LEFT
    def reset_character(self):
        super().reset_character()
        self._direction = Direction.LEFT
        self.__change_direction = None
