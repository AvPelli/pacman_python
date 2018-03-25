from enum import Enum


class Direction(Enum):
    # Possible directions a ghost or pacman can move
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, -1)
    DOWN = (0, 1)

    # Example to get the tuple
    # dir = Direction.LEFT
    # dir.value  --> (-1,0)

    """Getters"""

    # Getter: returns the first letter of the direction
    def get_letter(self):
        dicti = {Direction.LEFT: "l", Direction.RIGHT: "r", Direction.DOWN: "d", Direction.UP: "u"}
        return dicti[self]
