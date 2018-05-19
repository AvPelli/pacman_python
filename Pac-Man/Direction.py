from enum import Enum


class Direction(Enum):
    # Possible directions a ghost or pacman can move
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, -1)
    DOWN = (0, 1)
    BLOCK = (0, 0)

    # Example to get the tuple
    # dir = Direction.LEFT
    # dir.value  --> (-1,0)
    # Or with dir.x and dir.y

    def __init__(self, x, y):
        """
        Constructor: x and y value, these values sums up a direction
        :param x:
        :param y:
        """
        self.x = x
        self.y = y

    """Getters"""

    def get_letter(self):
        """
        Returns the first letter of the direction
        This method is used for the different movement images for pacman and ghosts
        :return: char
        """
        letters_dict = {Direction.LEFT: "l", Direction.RIGHT: "r", Direction.DOWN: "d", Direction.UP: "u"}
        return letters_dict[self]

    def get_reverse(self):
        """
        Returns the reverse direction of this one
        So Direction.RIGHT returns Direction.LEFT ect
        :return: Direction
        """
        reverse_dict = {Direction.LEFT: Direction.RIGHT, Direction.RIGHT: Direction.LEFT, Direction.DOWN: Direction.UP,
                        Direction.UP: Direction.DOWN, Direction.BLOCK: Direction.BLOCK}
        return reverse_dict[self]
