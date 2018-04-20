import math
from heapq import heappop, heappush

from Coordinate import Coordinate
from Direction import Direction


class Astar():

    def __init__(self, gates, bestand="res/files/maze2.txt"):
        self.__bestand = bestand
        self.gates = gates
        self.transporters = self.get_gates_coords_list(gates)
        self.maze = self.make_maze()
        self.graph = self.make_graph()
        self.dictionary = {"S": Direction.DOWN, "W": Direction.LEFT, "E": Direction.RIGHT, "N": Direction.UP}
        self.reverse_dict = {v: k for k, v in self.dictionary.items()}

    def make_maze(self):
        maze = list()
        input = [line.split() for line in open(self.__bestand, 'r')]
        for line in input:
            line_string = "".join(line).replace(" ", "").replace("\n", "")
            check = line_string.replace("0", "")
            if len(check) > 0:
                maze.append([0 if letter in "f0gG" or "t" in letter else 1 for letter in line])
        return maze

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

    def heuristic(self, cell, goal):
        minimum = self.manhattan_distance(cell, goal)
        for gate in self.gates:
            coord1, coord2 = gate.get_coordinates()
            waarde1 = self.manhattan_distance(cell, coord1.get_coord_tuple()) + \
                      self.manhattan_distance(coord2.get_coord_tuple(), goal)
            waarde2 = self.manhattan_distance(cell, coord2.get_coord_tuple()) + \
                      self.manhattan_distance(coord1.get_coord_tuple(), goal)
            minimum = min(minimum, waarde1, waarde2)

        return minimum

    def manhattan_distance(self, cell, goal):
        return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])

    def find_path(self, start_coord, goal_coord):
        pr_queue = []
        start, goal = start_coord.get_coord_tuple(), goal_coord.get_coord_tuple()
        heappush(pr_queue, (0 + self.heuristic(start, goal), 0, "", start))
        visited = set()
        while pr_queue:
            total_cost, cost, path, current_cell = heappop(pr_queue)
            if current_cell == goal:
                return path
            if current_cell not in visited:
                visited.add(current_cell)
                try:
                    for direction, neighbour in self.graph[current_cell]:
                        heappush(pr_queue, (cost + self.heuristic(neighbour, goal), cost + 1,
                                            path + direction, neighbour))
                except KeyError:
                    return self.failsafe(start, goal)
        return "No WAY"

    def get_direction(self, start, goal):
        path = self.find_path(start, goal)
        return self.dictionary[path[0]] if len(path) > 0 else None

    def get_gates_coords_list(self, gates):
        list_gates = list()
        for gate in gates:
            coord1, coord2 = gate.get_coordinates()
            list_gates.append(coord1)
            list_gates.append(coord2)

        return list_gates

    def print_maze(self):
        for x in range(len(self.maze)):
            out = ""
            for y in range(len(self.maze[x])):
                out += str(self.maze[x][y])
            print(out)

    def failsafe(self, start, goal):

        distance = math.inf
        x, y = start
        for dir in Direction:
            new_x, new_y = (x + dir.value[0], y + dir.value[1])
            # TODO Fix index out of bound error

            if not self.maze[new_y][new_x]:
                dis = self.manhattan_distance((new_x, new_y), goal)
                if dis < distance:
                    best_option = dir
                    distance = dis
        return self.reverse_dict[best_option]
