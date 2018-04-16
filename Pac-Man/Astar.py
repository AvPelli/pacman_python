from heapq import heappop, heappush

from Coordinate import Coordinate
from Direction import Direction


class Astar():

    def __init__(self):
        self.__bestand = "res/files/maze2.txt"
        self.maze = list()
        self.transporters = ((0, 14), (27, 14))
        self.makeMaze()
        self.map = {"S": Direction.DOWN, "W": Direction.LEFT, "E": Direction.RIGHT, "N": Direction.UP}

    def makeMaze(self):
        input = [line.split() for line in open(self.__bestand, 'r')]
        for line in input:
            hulp = list()
            zebra = "".join(line)
            zebra = zebra.replace(" ", "").replace("\n", "")
            check = zebra.replace("0", "")
            if len(check) > 0:
                for letter in line:
                    if letter in "f0t":
                        hulp.append(0)
                    else:
                        hulp.append(1)
                self.maze.append(hulp)

    def test_maze(self):
        for x in range(len(self.maze)):
            out = ""
            for y in range(len(self.maze[x])):
                out += str(self.maze[x][y])
            print(out)

    def maze2graph(self):
        maze = self.maze
        height = len(maze)
        width = len(maze[0]) if height else 0
        graph = {(j, i): [] for j in range(width) for i in range(height) if not maze[i][j]}
        for x, y in graph.keys():
            if (x, y) not in self.transporters:
                if y < height - 1:
                    if not maze[y + 1][x]:
                        graph[(x, y)].append(("S", (x, y + 1)))
                    if not maze[y - 1][x]:
                        graph[(x, y)].append(("N", (x, y - 1)))
                if x < width - 1:
                    if not maze[y][x - 1]:
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

    def manhattan_distance(self, cell, goal):
        return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])

    def heuristic(self, cell, goal):
        waarde1 = self.manhattan_distance(cell, goal)

        # Moet nog gefixt worden

        waarde2 = self.manhattan_distance(cell, (0, 14)) + self.manhattan_distance((27, 14), goal)
        waarde3 = self.manhattan_distance(cell, (27, 14)) + self.manhattan_distance((0, 14), goal)
        return min(waarde1, waarde2, waarde3)

    def find_path_astar(self, start_coord, goal_coord):
        pr_queue = []
        start,  goal = start_coord.get_coord_tuple(), goal_coord.get_coord_tuple()
        heappush(pr_queue, (0 + self.heuristic(start, goal), 0, "", start))
        visited = set()
        graph = self.maze2graph()
        while pr_queue:
            _, cost, path, current = heappop(pr_queue)
            if current == goal:
                return path
            if current not in visited:
                visited.add(current)
                for direction, neighbour in graph[current]:
                    heappush(pr_queue, (cost + self.heuristic(neighbour, goal), cost + 1,
                                        path + direction, neighbour))

        return "NO WAY!"

    def get_direction(self, start, goal):
        direction = self.find_path_astar(start, goal)[0]
        return self.map[direction]

astar = Astar()
print(astar.get_direction(Coordinate(21, 20), Coordinate(1, 14)))
