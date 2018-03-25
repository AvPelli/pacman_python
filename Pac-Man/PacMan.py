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

        # Variables for cosmetics
        self.__nummer = 1
        self.dict = self.__image_dict()
        self.__gameDisplay = game_display
        self.imageList = self.dict[self.__direction.getLetter()]
        self.__image = pg.image.load(
            "res/pacman/pacman-{letter} {number}.png".format(letter=self.__direction.getLetter(), number=self.__nummer))

        # Initializes Pacman on give start coordinate
        self.__game = game
        self.__gameDisplay.blit(self.__image, self.__coord.get_pixel_tuple())

        # Collision and direction control check variables
        self.walls = walls
        self.__change_direction = None

    """"Move method"""

    # The move method will move Pacman
    def move(self):
        # Checks if it needs to calculate a new coordinate
        # If Pacman is against a wall it will just redraw itself on the same coordinate, but there are not caluclations needed
        if not self.__moveable:
            self.__set_on_coord(self.__coord)
            return
        # Checks if the direction what was not possible a while ago is possible now
        self.__direction_waiter()
        # Caluclates a new coordinate
        new_coord = self.__calculate_new_coord()

        # Checks if the new coordinate is a wall
        # If it is a wall, it will not move ( as long as the direction isn't changed)
        # Else it will set the coordinate to the new one
        if new_coord in self.walls:
            self.__moveable = False
        else:
            self.__coord = new_coord
        # Moves to the new coordinate
        self.__set_on_coord(self.__coord)
        # Checks if there is candy to eat on the new coordinate
        self.__eat_candy()

    """"Check/Calculate Methods"""

    # This method will change the direction to the change_direction variable if it is possible
    # So when someone has pressed UP-key and it was not possible at that moment, this method will change the direction to UP
    # As soon as it is possible, therefor we check if pacmans its coordinates  added with the direction it would be change to is not a wall
    # If so it will change the moving direction
    def __direction_waiter(self):
        if self.__change_direction is not None and Coordinate(self.__coord.get_x() + self.__change_direction.value[0],
                                                              self.__coord.get_y() + self.__change_direction.value[
                                                                  1]) not in self.walls:
            self.__direction = self.__change_direction

    # Checks if there is a candy object on Pacmans coordinate
    # If so it will delete that Candy object out of the dictionary (So it will not be redrawn)
    def __eat_candy(self):
        candies = self.__game.get_candy_dict()
        if self.__coord in candies.keys():
            del self.__game.get_candy_dict()[self.__coord]
            self.score += 1

    # Calculates the new coordinate
    # It adds the coordinate changes by the direction to the original coordinate
    # Also this method checks if it is a "teleporter"
    def __calculate_new_coord(self):
        (maxX, maxY) = self.__game.get_max()
        (x, y) = (self.__coord.get_coord_tuple())
        addX, addY = self.__direction.value
        newX, newY = x + addX, y + addY
        if newX < -1:
            newX = maxX - 1
            self.__direction = Direction.LEFT
            self.__change_direction = self.__direction
        elif newX >= maxX - 1:
            newX = -1
            self.__direction = Direction.RIGHT
            self.__change_direction = self.__direction
        return Coordinate(newX, newY)

    """"Setters"""

    # Setter: this method sets the given direction
    # If the following coorinate (if you follows the given direction) is a wall
    # It will put the given direction in the change_direction variable (More info in __direction_changer methode)
    def set_direction(self, direction):
        if Coordinate(self.__coord.get_x() + direction.value[0],
                      self.__coord.get_y() + direction.value[1]) in self.walls:
            self.__change_direction = direction
            return
        self.__change_direction = None
        self.__direction = direction
        self.__moveable = True

    # Setter: It wil draw Pacman of the given coordinate
    def __set_on_coord(self, coordinate):
        (xPixels, yPixels) = (coordinate.get_pixel_tuple())
        self.__image = self.__get_image_direction(self.__direction)
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
