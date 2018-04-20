class Gate():

    def __init__(self, port1, port2):
        self.__port1 = port1
        self.__port2 = port2

    def get_coordinates(self):
        return self.__port1, self.__port2

    def give_other_port(self, port):
        return self.__port2 if port == self.__port1 else self.__port1

    def __eq__(self, other) -> bool:
        return (self.__port1 == other.__port1 and self.__port2 == other.__port2) or (
                self.__port1 == other.__port2 and self.__port2 == other.__port1)

    def __hash__(self) -> int:
        return self.__port1 * self.__port2
