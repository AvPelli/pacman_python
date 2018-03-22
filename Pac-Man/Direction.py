from enum import Enum


class Direction(Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, -1)
    DOWN = (0, 1)

    # Example to get the tuple
    # dir = Direction.LEFT
    # dir.value  --> (-1,0)

    def getLetter(self):
        dicti = {Direction.LEFT: "l", Direction.RIGHT: "r", Direction.DOWN: "d", Direction.UP: "u"}
        return dicti[self]
