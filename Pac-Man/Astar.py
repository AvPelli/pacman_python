import random
from heapq import heappop, heappush

from Coordinate import Coordinate
from Direction import Direction


class Astar():

    # Constructor for Astar algorithm
    def __init__(self, gates, pacman, file="res/files/maze2.txt"):
        self.__file = file
        self.gates = gates
        self.pacman = pacman
        self.transporters = self.get_gates_coords_list(gates)
        self.maze = self.make_maze()
        self.graph = self.make_graph()
        self.dictionary = {"S": Direction.DOWN, "W": Direction.LEFT, "E": Direction.RIGHT, "N": Direction.UP,
                           "B": Direction.BLOCK}
        self.reverse_dict = {v: k for k, v in self.dictionary.items()}
        # self.print_maze()
        # print("-----------------------------------------------------------------")

    # Makes a maze of the given file
    # A 1 stands for a wall or something pacman can't move through
    # A 0 stands for a place where pacman can walk/move to
    def make_maze(self):
        maze = list()
        input = [line.split() for line in open(self.__file, 'r')]
        for line in input:
            line_string = "".join(line).replace(" ", "").replace("\n", "")
            check = line_string.replace("0", "")
            # Filters whole lines of 0's, so only the real map (walls and walkable places) are into the maze
            if len(check) > 0:
                maze.append([0 if letter in "f0gPDG" or "t" in letter else 1 for letter in line])
        return maze

    # Makes a graph of the maze that was made in the method above
    # It is stored in a dictionary, it maps a tuple of coordinates on an array.
    # In this array there are tuples, first element is a direction like S(outh), W(est) ect, second element is the  a tuple of a coordinate in that specific direction
    # The items in the array are only items that Pac-Man can move to, so walls ect are not included in this graph
    # Example {(1,1) : [('S', (1, 2)), ('E', (2, 1))]}
    def make_graph(self):
        maze = self.maze
        height, width = len(maze), len(maze[0])
        graph = {(j, i): [] for j in range(width) for i in range(height) if not maze[i][j]}
        for x, y in graph.keys():
            if Coordinate(x, y) not in self.transporters:
                if y < height - 1:
                    if not maze[y + 1][x]:
                        graph[(x, y)].append(("S", (x, y + 1)))
                    if not maze[y - 1][x] and y - 1 >= 0:
                        graph[(x, y)].append(("N", (x, y - 1)))
                if x < width - 1:
                    if not maze[y][x - 1] and x - 1 >= 0:
                        graph[(x, y)].append(("W", (x - 1, y)))
                    if not maze[y][x + 1]:
                        graph[(x, y)].append(("E", (x + 1, y)))
            else:
                if x == 0:
                    graph[(x, y)].append(("W", (width - 1, y)))
                    graph[(x, y)].append(("E", (x + 1, y)))
                else:
                    graph[(x, y)].append(("W", (x - 1, y)))
                    graph[(x, y)].append(("E", (0, y)))
        return graph

    def test_graph(self):
        for coord in self.graph.keys():
            print("{coord} ---> {neigbours}".format(coord=coord, neigbours=self.graph[coord]))

    # Function that returns the manhattan distance between cell and goal
    # Cell and goal are both tuples like (1,1), NOT objects of the class Coordinate
    def manhattan_distance(self, cell, goal):
        return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])

    # This is an heuristic function this returns the minimal cost between cell and goal
    # It also takes the Gates into account, so if it is shoter to take a gate is will check it and return the smallest cost possible to go from cell to goal
    def heuristic(self, cell, goal):
        minimum = self.manhattan_distance(cell, goal)
        # Checks if it isn't shoter if a gate is used
        for gate in self.gates:
            coord1, coord2 = gate.get_coordinates()
            waarde1 = self.manhattan_distance(cell, coord1.get_coord_tuple()) + \
                      self.manhattan_distance(coord2.get_coord_tuple(), goal)
            waarde2 = self.manhattan_distance(cell, coord2.get_coord_tuple()) + \
                      self.manhattan_distance(coord1.get_coord_tuple(), goal)
            minimum = min(minimum, waarde1, waarde2)

        return minimum

    # Searches for the shortest (smallest cost path) path possible from start_coord to goal_coord
    # Both, start_coord and goal_coord, are objects of the class Coordinate
    def find_path(self, start_coord, goal_coord):
        pr_queue = []
        start, goal = start_coord.get_coord_tuple(), goal_coord.get_coord_tuple()
        heappush(pr_queue, (0 + self.heuristic(start, goal), 0, "", start))
        visited = set()
        while pr_queue:
            total_cost, cost, path, current_cell = heappop(pr_queue)
            if current_cell == goal:
                return path if len(path) > 0 else "B"
            if current_cell not in visited:
                visited.add(current_cell)
                try:
                    for direction, neighbour in self.graph[current_cell]:
                        heappush(pr_queue, (cost + self.heuristic(neighbour, goal), cost + 1,
                                            path + direction, neighbour))
                except:
                    print("ERRRRRRORRRR")
        return "NO PATH"

    def get_closest_tile(self, coord):
        coord_as_tuple = coord.get_coord_tuple()
        min = 1000
        result = None
        for tuple in self.graph.keys():
            hulp = self.manhattan_distance(coord_as_tuple, tuple)
            if hulp < min:
                min = hulp
                result = tuple
        return Coordinate(result[0], result[1])

    # Gives the first direction from the calculated path
    def get_direction(self, start, goal):
        pacCoord = self.pacman.get_coord()
        if (start == goal and goal != pacCoord):
            return self.choose_random(start)
        path = self.find_path(start, goal)
        if path is "":
            return self.choose_random(start)
        return self.dictionary[path[0]]

    def get_direction_scatter(self, start, goal):
        if (start == goal):
            return
        path = self.find_path(start, goal)
        if path is "":
            return self.choose_random(start)
        return self.dictionary[path[0]]

    def choose_random(self, coord):
        directions = self.get_possible_dir(coord)
        return directions[random.randint(0, len(directions) - 1)]

    def get_possible_dir(self, coord):
        possible_directions = []
        x, y = coord.get_coord_tuple()
        for dir in Direction:
            if dir is not Direction.BLOCK and (x + dir.value[0], y + dir.value[1]) in self.graph.keys():
                possible_directions.append(dir)
        return possible_directions

    """Getters"""

    # Getter: gives a list of coordinates that are gates
    def get_gates_coords_list(self, gates):
        list_gates = list()
        for gate in gates:
            coord1, coord2 = gate.get_coordinates()
            list_gates.append(coord1)
            list_gates.append(coord2)
        return list_gates

    # Test fucntion, it prints the maze
    def print_maze(self):
        for x in range(len(self.maze)):
            out = ""
            for y in range(len(self.maze[x])):
                out += str(self.maze[x][y])
            print(out)
