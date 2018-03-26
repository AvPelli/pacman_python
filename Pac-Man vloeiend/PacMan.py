import pygame as pg

from Coordinate import Coordinate
from Direction import Direction


class PacMan:
    # Constructor of PacMan
    def __init__(self, game_display, coordinate, game, walls):
        # Start variables
        self.score = 0
        self.__moveable = True
        self.__coord = coordinate
        self.__direction = Direction.RIGHT
        self.__moving_pos = 0
        self.__moving = False
        self.__PIXELSIZE = 16
        self.__speed = 2

        # Variables for cosmetics
        self.__nummer = 1
        self.dict = self.__image_dict()
        self.__gameDisplay = game_display
        self.imageList = self.dict[self.__direction.get_letter()]
        self.__image = pg.image.load(
            "res/pacman/pacman-{letter} {number}.png".format(letter=self.__direction.get_letter(),
                                                             number=self.__nummer))

        # Initializes Pacman on give start coordinate
        self.__game = game
        self.__gameDisplay.blit(self.__image, self.__coord.get_pixel_tuple())

        # Collision and direction control check variables
        self.walls = walls
        self.__change_direction = None

    """"Move method"""

    # The move method will move Pacman
    def move(self):
        # If pacman is moving between tiles, it will keep going that way until it reaches the next tile
        # Once there, it's coordinate will be updated so it's ready to be checked in the next iteration (will perform else)
        if self.__moving:
            self.__moving_pos += self.__speed
            self.__image = self.__get_image_direction(self.__direction)
            if self.__moving_pos >= 16:
                self.__moving_pos = 0
                self.__moving = False
                self.__coord.update_coord(self.__direction)
            self.__set_on_coord(self.__coord)
        # If pacman is not moving, meaning it's on 1 tile
        # Checks if it needs to calculate a new coordinate
        # If Pacman is against a wall it will just redraw itself on the same coordinate, but there are not caluclations needed
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
            # Else it can start moving there in the next iteration (will perform if self.__moving:)
            if check_next_coord in self.walls:
                self.__moveable = False
            else:
                if jump:
                    self.__set_on_opposite_side()
                self.__moving = True
            self.__set_on_coord(self.__coord)
            # Moves to the new coordinate
            # Checks if there is candy to eat on the new coordinate
            self.__eat_candy()

    # When Pacman reaches the edge of the map, its coordinates must be updated to the opposite side
    def __set_on_opposite_side(self):
        (maxX, maxY) = self.__game.get_max()
        (x, y) = (self.__coord.get_coord_tuple())
        if x < 0:
            self.__direction = Direction.LEFT
            self.__change_direction = self.__direction
            self.__coord = Coordinate(maxX, y)
        elif x > maxX:
            self.__direction = Direction.RIGHT
            self.__change_direction = self.__direction
            self.__coord = Coordinate(-2, y)

    """"Check/Calculate Methods"""

    # This method will change the direction to the change_direction variable if it is possible
    # So when someone has pressed UP-key and it was not possible at that moment, this method will change the direction to UP
    # As soon as it is possible, therefor we check if pacmans its coordinates  added with the direction it would be change to is not a wall
    # If so it will change the moving direction
    def __direction_waiter(self):
        if not self.__moving:
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
            self.score += 1000

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

    """"Setters"""

    # Setter: this method sets the given direction
    # If the following coorinate (if you follows the given direction) is a wall
    # It will put the given direction in the change_direction variable (More info in __direction_changer methode)
    def set_direction(self, direction):
        if Coordinate(self.__coord.get_x() + direction.value[0],
                      self.__coord.get_y() + direction.value[1]) in self.walls:
            self.__change_direction = direction
            return
        if self.__moving:
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
        self.__nummer = (self.__nummer + 1) % 8
        return pg.image.load(self.dict[direction.get_letter()][self.__nummer])

    """"Initialize methods """

    # Initialize the image dictionary
    def __image_dict(self):
        dict = {}
        for letter in "ldru":
            dict[letter] = list()
            for i in range(1, 10):
                dict[letter].append("res/pacman/pacman-{letter} {number}.png".format(letter=letter, number=i))
        return dict
