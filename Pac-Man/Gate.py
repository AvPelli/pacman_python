class Gate():

    def __init__(self, port1, port2):
        """
        Constructor of Gate (2 Coordinates are given)
        :param port1: type: Coordinate
        :param port2: type: Coordinate
        """
        self.__port1 = port1
        self.__port2 = port2

    def give_other_port(self, port):
        """
        Gives the other port, if port1 is given as parameter, this method will return port2 and vice versa
        :param port: type: Coordinate
        :return: Coordinate
        """
        return self.__port2 if port == self.__port1 else self.__port1

    """"Getters"""

    def get_coordinates(self):
        """
        Returns a tuple of coordinates which are part of this Gate
        :return: tuple
        """
        return self.__port1, self.__port2

    """Overwritten methods"""

    def __eq__(self, other) -> bool:
        """
        Override the equals method
        2 Gates object are the same if they the same 2 Coordinates
        :param other: type: Gate
        :return: boolean
        """
        return (self.__port1 == other.__port1 and self.__port2 == other.__port2) or (
                self.__port1 == other.__port2 and self.__port2 == other.__port1)

    def __hash__(self) -> int:
        """
        Override the hashcode
        :return: int
        """
        return self.__port1 * self.__port2
