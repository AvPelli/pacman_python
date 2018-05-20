import random
from heapq import heappop, heappush

import math

from Coordinate import Coordinate
from Direction import Direction


class Astar():

    # Constructor for Astar algorithm
    def __init__(self, gates, file="res/files/maze2.txt"):
        """
        Constructor of Astar\n
        Gates are used to see if there is a gate/transporter\n
        Pacman is used to use his coordinate if needed\n
        :param gates: type: List of Gates
        :param file: type: String
        There is a default file, but it is possible to change it with another file\n
        """
        self.__file = file
        self.__gates = gates
        self.__transporters = self.get_gates_coords_list(gates)
        self.__maze = self.make_maze()
        self.__graph = self.make_graph()
        self.dictionary = {"D": Direction.DOWN, "L": Direction.LEFT, "R": Direction.RIGHT, "U": Direction.UP,
                           "B": Direction.BLOCK}
        self.reverse_dict = {v: k for k, v in self.dictionary.items()}

    """Maze/Graph Methods"""

    def make_maze(self):
        """
        Makes a maze of the given file.\n
        A 1 stands for a wall or something pacman can't move through.\n
        A 0 stands for a place where pacman can walk/move to.\n
        :return: [][] (2 dimensional array)
        """
        maze = list()
        input_maze = [line.split() for line in open(self.__file, 'r')]
        for line in input_maze:
            line_string = "".join(line).replace(" ", "").replace("\n", "")
            check = line_string.replace("0", "")
            # Filters whole lines of 0's, so only the real maze (walls and walkable places) are into the maze
            # The 0 lines are only used for displaying lifes or the score ect, so these doesn't need to be in this maze
            if len(check) > 0:
                # All characters in the if statement are places where pacman can move to
                # These are hardcoded because the file structure used for the mazes should always be the same
                maze.append([0 if letter in "f0gPDG" or "t" in letter else 1 for letter in line])
        return maze

    def make_graph(self):
        """
        Makes a graph of the maze that was made in the method make_maze.\n
        It is stored in a dictionary, it maps a tuple of coordinates on an array.\n
        In this array there are tuples, first element is a direction like L(EFT), U(P) ect ...\n
        second element is the  a tuple of a coordinate in that specific direction.\n
        The items in the array are only items that Pac-Man can move to, so walls ect are not included in this graph.\n
        Example {(1,1) : [('D', (1, 2)), ('R', (2, 1))]}\n
        :return: {}  (Dictionary)
        """
        maze = self.__maze
        height, width = len(maze), len(maze[0])
        # The line below initializes the graph, all coordinates pacman can move to are mapped on a empty array
        # Example: { (1, 1) : [], (1, 2) : [] , ... }
        graph = {(x, y): [] for x in range(width) for y in range(height) if not maze[y][x]}
        for x, y in graph.keys():
            if Coordinate(x, y) not in self.__transporters:
                if y < height - 1:
                    if not maze[y + 1][x]:
                        graph[(x, y)].append(("D", (x, y + 1)))
                    if not maze[y - 1][x] and y - 1 >= 0:
                        graph[(x, y)].append(("U", (x, y - 1)))
                if x < width - 1:
                    if not maze[y][x - 1] and x - 1 >= 0:
                        graph[(x, y)].append(("L", (x - 1, y)))
                    if not maze[y][x + 1]:
                        graph[(x, y)].append(("R", (x + 1, y)))
            else:
                if x == 0:
                    graph[(x, y)].append(("L", (width - 1, y)))
                    graph[(x, y)].append(("R", (x + 1, y)))
                else:
                    graph[(x, y)].append(("L", (x - 1, y)))
                    graph[(x, y)].append(("R", (0, y)))
        return graph

    """A* Algorithm"""

    def find_path(self, start_coord, goal_coord):
        """
        A* algorithm:\n
        Searches for the shortest (smallest cost path) path possible from start_coord to goal_coord.\n
        Both, start_coord and goal_coord, are objects of the class Coordinate.\n
        :param start_coord: type: Coordinate
        :param goal_coord: type: Coordinate
        :return: string of smallest cost path
        """

        # The variable heap is like a stack, the first value will always be the one with the lowest cost path
        # This is due the heappush function, it will push a new item to the "heap" while remaining the heap invariant
        # The heap invariant here is the lowest total cost, so heap will be sorted on lowest to highest total cost paths
        heap = []
        start, goal = start_coord.get_coord_tuple(), goal_coord.get_coord_tuple()
        heappush(heap, (0 + self.heuristic(start, goal), 0, "", start))
        # The variable visited is a set of tuples, that already has been gone to
        visited = set()

        # The algorithm 'll stop if the heap is empty, if the heap is empty and so the current_cell is not the goal_cell
        # There is no path to connect the start and the goal cell and the algorithm will stop and return "NO PATH"
        while heap:
            total_cost, cost, path, current_cell = heappop(heap)

            # total_cost is the cost of (variable) path + the cost to go from the current_cell to the goal cell
            # cost is the cost of the calculated path, here cost = len(path) because every step add 1 to the cost of the path
            # path, is the path that takes you from the start coord to the current cell
            # current_cell, this is the cell you ended on if you follow the path and started on the start coord

            if current_cell == goal:
                return path if len(path) > 0 else "B"
            # The next statement is needed because if a current cell is already in visited it means there was a path before
            # that visited that cell. Because the heap is sorted on lowest total cost, that path was an already more promising
            # path, therefor there cannot be a path that visited that cell,later on the algorithm, and still be shorter
            if current_cell not in visited:
                visited.add(current_cell)
                try:
                    for direction, neighbour in self.__graph[current_cell]:
                        heappush(heap, (cost + self.heuristic(neighbour, goal), cost + 1,
                                        path + direction, neighbour))
                        # Adds the direction you need to take to go from the current cell to the neighbour cell to the path
                except:
                    # Normally, this doesn't appear. But when it does it will just skip it and recalculate everything the next time
                    pass
        return "NO PATH"

    """Hulp methods"""

    def manhattan_distance(self, cell, goal):
        """
        Function that returns the manhattan distance between cell and goal\n
        Cell and goal are both tuples like (1,1), NOT objects of the class Coordinate\n
        :param cell: type: tuple
        :param goal: type : tuple
        :return: int
        """
        return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])

    def heuristic(self, cell, goal):
        """
        This is an heuristic function this returns the minimal cost between cell and goal.\n
        It also takes the Gates into account, so if it is shorter to take a gate is will check it and return the smallest cost possible to go from cell to goal.\n
        :param cell: type: tuple
        :param goal: type: tuple
        :return: int
        """
        minimum = self.manhattan_distance(cell, goal)
        # Checks if it isn't shorter if a gate is used
        # Therefor all gates are checked, and the minimum of all of these values will be stored in the variable minimum
        for gate in self.__gates:
            coord1, coord2 = gate.get_coordinates()
            value1 = self.manhattan_distance(cell, coord1.get_coord_tuple()) + \
                     self.manhattan_distance(coord2.get_coord_tuple(), goal)
            value2 = self.manhattan_distance(cell, coord2.get_coord_tuple()) + \
                     self.manhattan_distance(coord1.get_coord_tuple(), goal)
            minimum = min(minimum, value1, value2)

        return minimum

    def choose_random(self, coord):
        """
        Return a random direction (that is possible).\n
        :param coord: type: Coordinate
        :return:  Direction
        """
        directions = self.get_possible_dir(coord)
        return directions[random.randint(0, len(directions) - 1)]

    """Getters"""

    # Some of these "getters" aren't real getters for a attribute but for something else
    # like getting specific items or data structures ect, ...
    def get_direction(self, start, goal):
        """
        Gives the first direction from the calculated path.\n
        :param start: type: Coordinate
        :param goal: type: Coordinate
        :return: Direction
        """
        path = self.find_path(start, goal)
        if path is "" or path is "B":
            return self.choose_random(start)
        return self.dictionary[path[0]]

    def get_closest_tile(self, coord):
        """
        This method calculate a coordinate closed by the given coordinate.\n
        Only when the given coord is not a part of the graph.\n
        :param coord: type: Coordinate
        :return: Coordinate
        """
        coord_as_tuple = coord.get_coord_tuple()
        if coord_as_tuple in self.__graph.keys():
            return coord

        result = None
        minimum_distance = math.inf
        for possibility in self.__graph.keys():
            distance = self.manhattan_distance(coord_as_tuple, possibility)
            if distance < minimum_distance:
                minimum_distance = distance
                result = possibility

        return Coordinate(result[0], result[1])

    def get_gates_coords_list(self, gates):
        """
        Gives a list of coordinates that are gates.\n
        :param gates: type: list of Gates
        :return: list of Coordinates
        """
        list_gates = list()
        for gate in gates:
            coord1, coord2 = gate.get_coordinates()
            list_gates.append(coord1)
            list_gates.append(coord2)
        return list_gates

    def get_possible_dir(self, coord):
        """
        Gives an array of the possible directions that a ghost can make in a given coordinate.\n
        :param coord: type: Coordinate
        :return: [] of Directions
        """
        possible_directions = []
        x, y = coord.get_coord_tuple()
        for direction in Direction:
            if direction is not Direction.BLOCK and \
                    (x + direction.value[0], y + direction.value[1]) in self.__graph.keys():
                possible_directions.append(direction)
        return possible_directions

    """Test/Print Methods"""

    def print_maze(self):
        """
        Test method, it prints the maze.\n
        :return: void
        """
        for x in range(len(self.__maze)):
            out = ""
            for y in range(len(self.__maze[x])):
                out += str(self.__maze[x][y])
            print(out)

    def print_graph(self):
        """
        Test method, it prints the graph.\n
        :return: void
        """
        for coord in self.__graph.keys():
            print("{coord} ---> {neigbours}".format(coord=coord, neigbours=self.__graph[coord]))
