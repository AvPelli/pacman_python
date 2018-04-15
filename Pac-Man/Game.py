import pygame as pg  # Importeren van pg module

from Direction import Direction
from Map import Map
from PacMan import PacMan

black = (0, 0, 0)
tile_size = 16
resolution = (448, 576)

clock = pg.time.Clock()


class Game():
    # Constructor of Game
    def __init__(self):
        # Init of pygame
        pg.init()
        pg.display.set_caption('Pac-Man')

        # Game variables
        self.gamemode = 2
        self.pauze = False
        self.gameExit = False
        self.game_display = pg.display.set_mode(resolution)

        # Music settings
        self.intro_played = False

        # Game objects
        self.map = Map(self.game_display, resolution[0], resolution[1], tile_size)
        self.clock = pg.time.Clock()
        self.candies = self.map.get_candy_dict()
        self.pacman = PacMan(self.game_display, self.map.get_pacman_start(), self, self.map.get_wall_list())

        # Link objects
        self.map.set_pacman(self.pacman)

    # Setting up the game - press a  KEY to start
    def gamemode2(self):
        # Draw methods, be aware of the sequence!
        self.map.draw_map()
        self.map.draw_candy()
        self.map.draw_startpacman()
        self.map.draw_readytext()
        self.map.draw_oneup()
        pg.display.update()
        self.clock.tick(50)

        # Music methods
        if not (self.intro_played):
            self.SONG_END = pg.USEREVENT + 1
            pg.mixer.music.set_endevent(self.SONG_END)
            pg.mixer.music.load("res/files/music/pacman-beginning/pacman_beginning.wav")
            pg.mixer.music.play()
            self.intro_played = True
        # Event check, quit event check first
        self.check_quit_events()
        self.check_beginningmusic_events()

    # Gaming
    def gamemode3(self):
        self.game_display.fill(black)
        self.map.draw_map()
        self.map.draw_candy()
        self.pacman.move()
        self.map.draw_oneup()
        pg.display.update()
        self.clock.tick(50)
        # Event check, quit event check first
        self.check_key_events()
        self.check_quit_events()

    def gamemode_handler(self):
        if self.gamemode == 2:
            self.gamemode2()
        elif self.gamemode == 3:
            self.gamemode3()

    """"Getters"""

    # Getter: returns dictionary, Coordinate mapped on a Candy object
    def get_candy_dict(self):
        return self.candies

    # Getter: returns max amount of colums and rows
    def get_max(self):
        return self.map.tiles_horiz_size-1, self.map.tiles_vert_size-1

    """"Events"""

    def check_quit_events(self):
        for event in pg.event.get(pg.QUIT):
            print("hier")
            self.gameExit = True

    def check_key_events(self):
        for event in pg.event.get(pg.KEYDOWN):
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

    def check_beginningmusic_events(self):
        for event in pg.event.get(self.SONG_END):
            self.gamemode = 3
            self.map.remove_readytext()

    """"Main method"""

    # This is the main method
    # It catches every input from the keyboard
    # Also it functions as a kind of timeline everything in the while loop will be exectued as long as the game hasn't stopped
    def run(self):
        while not self.gameExit:
            # If the game is not paused, the game wil continue
            if not (self.pauze):
                self.gamemode_handler()
            else:
                for event in pg.event.get(pg.KEYDOWN):
                    # Pauze button: p
                    if event.key == pg.K_p:
                        self.pauze = False
            self.check_quit_events()

        pg.quit()
        quit()
