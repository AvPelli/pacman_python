import pygame as pg

from Coordinate import Coordinate
from Direction import Direction


class PacMan:
    # Constructor of PacMan
    def __init__(self, game_display, coordinate, game, walls):
        # Start variables
        self.score = 0
        self.lifes = 2
        self.__moveable = True
        self.__coord = coordinate
        self.__direction = Direction.RIGHT
        self.__moving_pos = 0
        self.__moving_between_tiles = False
        self.__PIXELSIZE = 16
        self.__speed = 2
        self.__turnaround = False

        # Variables for cosmetics
        self.__number = 1
        self.dict = self.__image_dict()
        self.__gameDisplay = game_display
        self.__game = game
        self.imageList = self.dict[self.__direction.get_letter()]
        self.__image = pg.image.load(
            "res/pacman/pacman-{letter} {number}.png".format(letter=self.__direction.get_letter(),
                                                             number=self.__number))

        # Collision and direction control check variables
        self.walls = walls
        self.__change_direction = None

    # Initializes Pacman on give start coordinate
    def draw_pacman(self):
        self.__gameDisplay.blit(self.__image, self.__coord.get_pixel_tuple())

    """"Move method"""

    # The move method will move Pacman
    def move(self):
        # If pacman is moving between tiles, it will keep going that way until it reaches the next tile
        if self.__moving_between_tiles:
            self.__check_turnaround()
            self.__move_between_tiles()

        # If pacman is not moving, meaning it's on 1 tile exactly, will perform this
        # If Pacman is against a wall it will just redraw itself on the same coordinate, but there are not caluclations needed
        # Else it checks if it needs to calculate a new coordinate, and if a different direction input has been given
        else:
            if not self.__moveable:
                self.__set_on_coord(self.__coord)
                return
            # Checks if the direction what was not possible a while ago is possible now
            self.__direction_waiter()
            # Calculates the next coordinate
            check_next_coord, jump = self.__calculate_new_coord()

            # Checks if the new coordinate is a wall
            # If it is a wall, it will not move ( as long as the direction isn't changed)
            # Else it can start moving there in the next iteration (will perform if self.__moving_between_tiles:)
            if check_next_coord in self.walls:
                self.__moveable = False
            else:
                if jump:
                    self.__set_on_opposite_side()
                self.__moving_between_tiles = True
            self.__set_on_coord(self.__coord)
            # Moves to the new coordinate
            # Checks if there is candy to eat on the new coordinate
            self.__eat_candy()

    def __move_between_tiles(self):
        if not self.__turnaround:
            # Proceed to the next tile
            self.__image = self.__get_image_direction(self.__direction)
            self.__moving_pos += self.__speed
            if self.__moving_pos >= 16:
                self.__moving_pos = 0
                self.__moving_between_tiles = False
                # Once there, it's coordinate will be updated so it's ready to be checked in the else: part of move
                self.__coord.update_coord(self.__direction)
        # However if turnaround has been set (see check_turnaround), pacman will have to move back to the beginning his original tile 1st
        # Once there he'll set himself ready for the next iteration (and its coordinate will NOT be updated)
        # To solve issues bug-wise, number will be set on 0 once it has moved back, so its beak is closed at the end, as usual
        # Also note that, while the image will be reversed, pacman's direction will not be updated until he has finished moving so prevent extra issues that cause all sorts of headaches
        else:
            self.__image = self.__get_image_direction(self.__change_direction)
            self.__moving_pos -= self.__speed
            if self.__moving_pos <= 0:
                self.__moving_pos = 0
                self.__moving_between_tiles = False
                self.__turnaround = False
                self.__number = 0
        self.__set_on_coord(self.__coord)

    # When Pacman reaches the edge of the map, its coordinates must be updated to the opposite side
    def __set_on_opposite_side(self):
        (maxX, maxY) = self.__game.get_max()
        (x, y) = (self.__coord.get_coord_tuple())
        if x < 0:
            self.__direction = Direction.LEFT
            self.__coord = Coordinate(maxX, y)
        elif x > maxX:
            self.__direction = Direction.RIGHT
            self.__coord = Coordinate(-2, y)

    """"Check/Calculate Methods"""

    # This method will change the direction to the change_direction variable if it is possible
    # So when someone has pressed UP-key and it was not possible at that moment, this method will change the direction to UP
    # As soon as it is possible, therefor we check if pacmans its coordinates  added with the direction it would be change to is not a wall
    # If so it will change the moving direction
    def __direction_waiter(self):
        if not self.__moving_between_tiles:
            if self.__change_direction is not None and Coordinate(
                    self.__coord.get_x() + self.__change_direction.value[0],
                    self.__coord.get_y() + self.__change_direction.value[
                        1]) not in self.walls:
                self.__direction = self.__change_direction

    # Checks if there is a candy object on Pacmans coordinate
    # If so it will delete that Candy object out of the dictionary (So it will not be redrawn)
    def __eat_candy(self):
        candies = self.__game.get_candy_dict()
        if self.__coord in candies.keys():
            del self.__game.get_candy_dict()[self.__coord]
            self.score += 10

    # Calculates the next coordinate
    # Also this method checks if it is a "teleporter" which will perform __set_on_opposite_side() in move() method
    def __calculate_new_coord(self):
        (maxX, maxY) = self.__game.get_max()
        (x, y) = (self.__coord.get_coord_tuple())
        addX, addY = self.__direction.value
        newX, newY = x + addX, y + addY
        jump = False
        if newX < -2 or newX > maxX:
            jump = True
        return Coordinate(newX, newY), jump

    # When pacman is moving between tiles, he should still be able to immediately turn around instead of finishing moving to the next tile 1st,
    # This method will check if an opposite key has been pressed and sets the variable __turnaround
    def __check_turnaround(self):
        if self.__change_direction is not None:
            x_direction = self.__direction.value[0] + self.__change_direction.value[0]
            y_direction = self.__direction.value[1] + self.__change_direction.value[1]
            self.__turnaround = x_direction == 0 and y_direction == 0
        return None

    """"Setters"""

    # Setter: this method sets the given direction
    # If the following coorinate (if you follows the given direction) is a wall
    # It will put the given direction in the change_direction variable (More info in __direction_changer methode)
    def set_direction(self, direction):
        if Coordinate(self.__coord.get_x() + direction.value[0],
                      self.__coord.get_y() + direction.value[1]) in self.walls:
            self.__change_direction = direction
            return
        if self.__moving_between_tiles:
            self.__change_direction = direction
        else:
            self.__change_direction = None
            self.__direction = direction
            self.__moveable = True

    # Setter: It wil draw Pacman of the given coordinate
    def __set_on_coord(self, coordinate):
        (xPixels, yPixels) = (coordinate.get_pixel_tuple())
        xPixels += self.__direction.value[0] * self.__moving_pos
        yPixels += self.__direction.value[1] * self.__moving_pos

        self.__gameDisplay.blit(self.__image, (xPixels, yPixels))

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

    # Returns the amount of lifes left
    def getLifes(self):
        return self.lifes

    # Returns the score
    def getScore(self):
        return self.score
