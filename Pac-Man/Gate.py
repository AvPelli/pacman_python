class Gate():

    # Constructor of Gate (2 Coordinates are given)
    def __init__(self, port1, port2):
        self.__port1 = port1
        self.__port2 = port2

    # Gives the other port, if port1 is given with this method it will return port2 and vice versa
    def give_other_port(self, port):
        return self.__port2 if port == self.__port1 else self.__port1

    """"Getters"""

    # Getter: returns a tuple of coordinates which are part of this Gate
    def get_coordinates(self):
        return self.__port1, self.__port2

    """Overwritten methods"""

    # Override the equals method
    # 2 Gates object are the same if they the same 2 Coordinates
    def __eq__(self, other) -> bool:
        return (self.__port1 == other.__port1 and self.__port2 == other.__port2) or (
                self.__port1 == other.__port2 and self.__port2 == other.__port1)

    # Override the hashcode
    def __hash__(self) -> int:
        return self.__port1 * self.__port2
