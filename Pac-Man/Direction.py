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
        self.x = x
        self.y = y

    """Getters"""

    # Getter: returns the first letter of the direction
    def get_letter(self):
        """
        Getter
        :return: char
        """
        letters_dict = {Direction.LEFT: "l", Direction.RIGHT: "r", Direction.DOWN: "d", Direction.UP: "u"}
        return letters_dict[self]

    def get_reverse(self):
        """
        Getter
        :return: dictionary
        """
        reverse_dict = {Direction.LEFT: Direction.RIGHT, Direction.RIGHT: Direction.LEFT, Direction.DOWN: Direction.UP,
                        Direction.UP: Direction.DOWN, Direction.BLOCK: Direction.BLOCK}
        return reverse_dict[self]
