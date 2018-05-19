import pygame as pg  # Importeren van pygame module

from Candy import Candy
from Coordinate import Coordinate
from Gate import Gate
from SuperCandy import SuperCandy


class Maze:

    # Constructor of Maze

    def __init__(self, game, width, height, tile_size):
        """
        Creates a Maze, which draws the actual map and supervises most of the objects in the game.\n
        It reads in a standard text file from which it will create the whole map and determines where everything\n
        has to be located, by giving everything appropriate Coordinates.\n
        :param game: the game that created this maze
        :param width: maze width (in pixels)
        :param height: maze height (in pixels)
        :param tile_size: the length of a rib of the square that defines a tile (in pixels)
        """
        # Amount of rows en colums
        self.__tiles_horiz_size = 28
        self.__tiles_vert_size = 36

        # Screen and Resolution variables
        self.__game = game
        self.__game_display = self.__game.get_game_display()  # The display of the game
        self.__width = width
        self.__height = height
        self.__tile_size = tile_size

        # Makes dictionary, maps  a Character on an specific image
        self.__tiles = {}
        self.__init_tiles()

        # Makes the tilemap
        filename = "res/files/maze2.txt"
        self.__maze = [line.split() for line in open(filename, 'r')]

        # Item lists/ditcionaries
        self.__coord_dict = {}
        self.__candy_dict = {}
        self.__ghosts_coord = list()
        self.__init_items()

        # Pacman himself
        self.__pacman = None

        # Font settings
        self.font_obj = pg.font.Font("res/files/fonts/emulogic.ttf", 16)
        self.oneup = True
        self.fontoffset = 3

        # Maze settings
        self.clock = pg.time.Clock()
        self.upcounter = 0

    """Draw Methods"""

    def draw_maze(self):
        """
        Draws all the walls of the maze.\n
        :return: void
        """
        for row in range(0, self.__tiles_vert_size):
            for col in range(0, self.__tiles_horiz_size):  # = Amount of tiles in 1 row
                tile_sign = self.__maze[row][col]
                self.__game_display.blit(self.__tiles[tile_sign], (col * self.__tile_size, row * self.__tile_size))
        self.draw_extra()

    def draw_extra(self):
        """
        Draws all the 'extras', like Pacman's lifes, and it's score. Uses the other drawing methods.\n
        :return: void
        """
        self.draw_lifes()
        self.draw_text("HIGHSCORE", 9, 0, (0, 255, 0))
        # self.draw_grid()
        self.draw_score()

    # Method for drawing the amount of lives pacman has left
    def draw_lifes(self):
        """
        Draws Pacman's lifes in the bottom left corner of the screen.\n
        :return: void
        """
        width = self.__tile_size * 2
        height = self.__tile_size * (self.__tiles_vert_size - 2)
        lifesimg = pg.image.load("res/tileset/pacman_lifes.png")
        img_width = lifesimg.get_width()
        for i in range(0, self.__pacman.get_lifes()):
            self.__game_display.blit(lifesimg, (width, height))
            width += img_width

    # Draw text with a given coordinate and color(as a tuple). x en y depends on the tile_size
    def draw_text(self, text, x, y, color_rgb=(255, 255, 255)):
        """
        Draws any given text onto the screen, requires extra params for location.\n
        :param text: the text that should be drawn
        :param x: the starting x-coordinate (in tiles)
        :param y: the y-coordinate (in tiles)
        :param color_rgb: in which color (tuple with rgb values) the text should be drawn (standard white)
        :return: void
        """
        text_surface_obj = self.font_obj.render(text, False, color_rgb)
        self.__game_display.blit(text_surface_obj, (x * self.__tile_size, y * self.__tile_size - self.fontoffset))

    def draw_oneup(self):
        """
        Draws the '1UP' text in the top of the screen and makes it switch colors.\n
        :return: void
        """
        duration = 60
        if self.upcounter < duration:
            self.oneup = False
            self.draw_text('1UP', 3, 0, (255, 0, 0))
            self.upcounter += 1
        elif duration <= self.upcounter < duration * 2:
            self.oneup = True
            self.draw_text('', 3, 0)
            self.upcounter += 1
            if self.upcounter == duration * 2:
                self.upcounter = 0

    # Method for drawing the score
    def draw_score(self):
        """
        Draws Pacman's current score.\n
        :return: void
        """
        score = self.__pacman.get_score()
        scorestr = str(self.__pacman.get_score())
        if score < 10:
            scorestr = str(0) + scorestr
        score_size = len(scorestr)
        text_surface_obj = self.font_obj.render(scorestr, False, (255, 255, 255))
        self.__game_display.blit(text_surface_obj,
                                 (7 * self.__tile_size - score_size * 16, self.__tile_size - self.fontoffset))

    def draw_grid(self):
        """
        Draws a grid over the whole map, which makes it easy to see every tile/coordinate.\n
        Toggled in the draw_extra method (Handy for debugging ect).\n
        :return: void
        """
        # (200, 10, 20): is kleur rood
        # pg.draw.line(self.gameDisplay, (200, 10, 20), (0, self.__tile_size), (self.__width, self.__tile_size))
        for x in range(0, self.__tiles_horiz_size):
            pg.draw.line(self.__game_display, (169, 169, 169), (self.__tile_size * x, 0),
                         (self.__tile_size * x, self.__height))
        for y in range(0, self.__tiles_vert_size):
            pg.draw.line(self.__game_display, (169, 169, 169), (0, self.__tile_size * y),
                         (self.__width, self.__tile_size * y))

    def draw_pacmandeathani(self, dead_coord):
        """
        Draws Pacman's death animation on screen.\n
        :param dead_coord: the coordinate where pacman has been eaten
        :return: void
        """
        imagefolder = "res/pacmandeath/"
        for x in range(1, 12):
            pg.time.delay(100)
            self.draw_allsteadyparts()
            pacmanimgdeath = pg.image.load(imagefolder + str(x) + ".png")
            self.__game_display.blit(pacmanimgdeath, dead_coord.get_pixel_tuple())

            pg.display.update()

    def draw_candy(self):
        """
        Draws all candies left on screen by iterating over it's candy list.\n
        :return: void
        """
        self.draw_maze()
        for candy in self.__candy_dict.values():
            candy.draw(candy.get_coord())

    def draw_maze_with_candy(self):
        """
        Draws both the walls and the candies, uses the other drawing methods.\n
        :return: void
        """
        self.draw_maze()
        self.draw_candy()

    def draw_allsteadyparts(self):
        """
        Draws both the maze and all the text by using the other drawing methods.\n
        :return: void
        """
        self.draw_maze_with_candy()
        self.draw_score()
        self.draw_oneup()

    def draw_todisplay(self):
        """
        Updates the current screen, draws everything that has been blit up until now.\n
        :return: void
        """
        pg.display.update()

    def change_wall_color(self, won=True):
        """
        Changes the current color in which the walls are drawn, by loading a different image instead\n
        of the normal blue image.\n
        :param won: type: boolean:  use a white variant of the walls
        :return: void
        """
        filename = "res/files/tile_codering.txt"
        for line in open(filename, 'r'):
            sign_tilename = line.strip().split(" : ")
            if won:
                tile_name = "res/tileset/Game-won/" + sign_tilename[1] + ".png"
            else:
                tile_name = "res/tileset/" + sign_tilename[1] + ".png"

            self.__tiles[sign_tilename[0]] = pg.image.load(tile_name)

    """Initialize methods"""

    # Initialize all the items:
    # *   Makes a dictionary {Coordinate : Candy}
    # *   Initialise PacMan start coordinate
    # *   Makes a list of coordinates where there are walls
    def __init_items(self):
        """
        Initializes most of the data-structures the Maze will hold, is called in __init__\n
        It will process the contents of the text file and decode every char into the right object,\n
        while also filling it's coord dictionary, which projects every (x,y) tuple onto the coordinate-object\n
        with that location.\n
        :return: void
        """
        maze_noborders = self.__maze[3:]
        self.__gates_dict = {}
        self.gate_list = list()
        for y in range(0, len(maze_noborders)):
            for x in range(0, len(maze_noborders[0])):
                self.__coord_dict[(x, y)] = Coordinate(x, y)
                coord = self.__coord_dict.get((x, y))
                if maze_noborders[y][x] == "f":  # Place where candy show be drawn
                    self.__candy_dict[coord] = (Candy(self.__game_display, coord))
                elif maze_noborders[y][x] == "D":
                    self.__candy_dict[coord] = (SuperCandy(self.__game_display, coord))
                elif maze_noborders[y][x] == "P":  # Place where PacMan needs to be located
                    self.__pacman_coord = coord
                elif maze_noborders[y][x] in "/=.-_\éè\()}{][abcd12345678uijonq":  # All the characters that are walls
                    del self.__coord_dict[(x, y)]
                    self.__coord_dict[(x, y)] = Coordinate(x, y, True)
                elif maze_noborders[y][x] == 'g':
                    self.__ghosts_coord.append(coord)
                elif "t" in maze_noborders[y][x]:
                    # At a teleporter, add some "fake" walls to the list to make sure pacman doesn't go out of bounds
                    self.add_gate(maze_noborders[y][x], coord)

        self.make_gate_list()

    def __init_tiles(self):
        """
        Initializes a dictionary that projects every character onto the right tile image, is needed for init_tiles.\n
        :return: void
        """
        filename = "res/files/tile_codering.txt"
        for line in open(filename, 'r'):
            sign_tilename = line.strip().split(" : ")
            tile_name = "res/tileset/" + sign_tilename[1] + ".png"
            self.__tiles[sign_tilename[0]] = pg.image.load(tile_name)

    """Getters"""

    def get_coord_dict(self):
        """
        Returns the coord dictionary, which holds every coordinate of the map.\n
        :return: {} of Coordinates
        """
        return self.__coord_dict

    # Getter: returns a copy of pacman his start coordinate
    def get_pacman_start(self):
        """
        Returns pacman's start-coordinate.\n
        :return: coordinate
        """
        return self.__pacman_coord

    def get_ghosts_start(self):
        """
        Returns the ghosts' starting coordinates.\n
        :return: list
        """
        return self.__ghosts_coord

    def get_candy_dict(self):
        """
        Returns the whole candy dictionary, containing every candy that has not been eaten by now.\n
        :return: dictionary
        """
        return self.__candy_dict

    def get_gates(self):
        """
        Returns all gates as a list, not as a dictionary.\n
        :return: list
        """
        return self.gate_list

    def get_tiles_horiz_size(self):
        """
        Returns how many tiles across (horizontally) the map is.\n
        :return: int
        """
        return self.__tiles_horiz_size

    def get_tiles_vert_size(self):
        """
        Returns how many tiles across (vertically) the map is.\n
        :return: int
        """
        return self.__tiles_vert_size

    def get_candy_amount(self):
        """
        Returns how many candies are currently left on the map.\n
        :return: int
        """
        return len(self.__candy_dict)

    """Setters"""

    # Setter: sets the pacman object

    def set_pacman(self, p):
        """
        Give the map this Pacman object to track, is used to get this Pacman's lives and score so it can draw them.\n
        :param p: Pacman
        :return: void
        """
        self.__pacman = p

    def add_gate(self, gate_number, coordinate):
        """
        Add a gate to the right list in the gate dictionary, the dictionary's used to know which gates work together.\n
        :param gate_number: the gate couple's ID
        :param coordinate: where this gate is on the map
        :return:
        """
        if len(self.__gates_dict.keys()) == 0 or gate_number not in self.__gates_dict.keys():
            self.__gates_dict[gate_number] = list()
        self.__gates_dict[gate_number].append(coordinate)

    def make_gate_list(self):
        """
        Forms a separate list of the existing gates, rather than having them in separate lists in a dictionary.\n
        :return: void
        """
        for gate_number in self.__gates_dict:
            self.gate_list.append(Gate(self.__gates_dict[gate_number][0], self.__gates_dict[gate_number][1]))
