import pygame as pg  # Importeren van pg module

from Direction import Direction
from Map import Map
from PacMan import PacMan

width = 224 * 2
height = 288 * 2
tile_size = 8 * 2
black = (0, 0, 0)
resolution = (width, height)

game_display = pg.display.set_mode(resolution)
pg.display.set_caption('Pac-Man')
clock = pg.time.Clock()


class Game():
    # Constructor of Game
    def __init__(self):
        pg.init()  # Init of pg
        self.game_display = pg.display.set_mode(resolution)
        self.map = Map(self.game_display, width, height, tile_size)
        self.map.draw_map()
        self.clock = pg.time.Clock()
        self.candies = self.map.get_candy_dict()
        self.pacman = PacMan(self.game_display, self.map.get_pacman_start(), self, self.map.get_wall_list())

    """Draw methods"""

    # Redraws the whole game
    def redraw(self):
        self.game_display.fill(black)
        self.map.redraw_everything()
        self.pacman.move()
        pg.display.update()
        self.clock.tick(50)

    """"Getters"""

    # Getter: returns dictionary, Coordinate mapped on a Candy object
    def get_candy_dict(self):
        return self.candies

    # Getter: returns max amount of colums and rows
    def get_max(self):
        return width / tile_size, height / tile_size

    """"Main method"""

    # This is the main method
    # It catches every input from the keyboard
    # Also it functions as a kind of timeline everything in the while loop will be exectued as long as the game hasn't stopped
    def run(self):
        gameExit = False
        self.pauze = False
        while not gameExit:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    gameExit = True
                if event.type == pg.KEYDOWN:
                    # Pauze button: p
                    if event.key == pg.K_p:
                        self.pauze = True if self.pauze == False else False
                    # Sends the direction input to Pacman
                    elif event.key == pg.K_LEFT:
                        self.pacman.set_direction(Direction.LEFT)
                    elif event.key == pg.K_RIGHT:
                        self.pacman.set_direction(Direction.RIGHT)
                    elif event.key == pg.K_UP:
                        self.pacman.set_direction(Direction.UP)
                    elif event.key == pg.K_DOWN:
                        self.pacman.set_direction(Direction.DOWN)
            # If the game is not paused, it will redraw the whole game
            if not self.pauze:
                self.redraw()
        pg.quit()
        quit()


# Let the game start
game = Game()
game.run()
