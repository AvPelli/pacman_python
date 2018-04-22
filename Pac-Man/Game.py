import pygame as pg  # Importeren van pg module

from Direction import Direction
from Ghost import Ghost
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
        self.gamemode = 1
        self.pauze = False
        self.gameExit = False
        self.game_display = pg.display.set_mode(resolution)
        self.pacmanCaught = False

        # Music settings
        self.intro_played = False

        # Startscreen settings
        self.mainmenuExit = False

        # Game objects
        self.map = Map(self.game_display, resolution[0], resolution[1], tile_size)
        self.clock = pg.time.Clock()
        self.candies = self.map.get_candy_dict()
        self.pacman = PacMan(self.game_display, self.map.get_pacman_start(), self, self.map.get_wall_list())

        self.ghosts = []
        starting_positions = self.map.get_ghosts_start()
        for i in starting_positions:
            self.ghosts.append(Ghost(self.game_display, i, self, self.map.get_wall_list()))
        # Link objects
        self.map.set_pacman(self.pacman)

    def gamemode_handler(self):
        if self.gamemode == 1:
            self.start_screen()
        elif self.gamemode == 2:
            self.ready_screen()
        elif self.gamemode == 3:
            self.play_screen()
        elif self.gamemode == 4:
            self.reset_screen()
        elif self.gamemode == 5:
            self.gameover_screen()

    # Startscreen mode - game displays startscreen
    def start_screen(self):
        # self.game_display.fill(Game.black)
        startscreen_image = pg.image.load("res/startscreen/startscreen.jpg")
        self.game_display.blit(startscreen_image, (0, 125))
        pg.display.flip()

        self.clock.tick(10)

        # Event check, quit event check first
        self.check_x_event()
        self.check_quit_events()

    # Setting up the game - press a  KEY to start

    def ready_screen(self):
        # Draw methods, be aware of the sequence!
        self.map.draw_candy()
        self.map.draw_startpacman(self.map.get_pacman_start())
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
    def play_screen(self):
        self.game_display.fill(black)
        self.map.draw_candy()
        self.pacman.move()
        for ghost in self.ghosts:
            ghost.move()
        self.map.draw_oneup()
        pg.display.update()
        self.clock.tick(60)
        # Event check, quit event check first
        self.check_move_events()
        self.check_quit_events()
        self.check_pacman_caught()

        if (self.pacmanCaught):
            lifes = self.pacman.getLifes() - 1
            self.pacman.set_lifes(lifes)
            self.pacmanCaught = False
            self.gamemode = 4  # reset the game: ghosts in center and pacman in middle

        if not (self.pacman.getLifes()):
            self.gamemode = 5  # no more lifes left: game over

    def reset_screen(self):
        pg.time.delay(1000)  # wait 1 second

        # pacman back to the starting position
        self.pacman.reset_character()

        # ghosts back to starting position
        self.reset_ghosts()
        self.gamemode = 3

    def gameover_screen(self):
        pg.time.delay(1000)
        self.game_display.fill(black)
        self.map.draw_candy()
        self.map.draw_oneup()
        pg.display.update()
        deathco = self.pacman.getCoord()
        self.map.draw_pacmandeathani(deathco)
        pg.display.update()

        # Event check, quit event check first
        self.check_quit_events()
        self.gameExit=True

        """"
        gamemode4_exit = False
        while not gamemode4_exit:
            # check for QUIT or "X" to play another game
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    gamemode4_exit = True
                    pg.quit()

                # Restart startscreen:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_x:
                        pg.quit()
                        gamemode4_exit = True
                        # Startscreen = gamemode 1
                        self.gamemode = 1
        """

    def check_pacman_caught(self):
        for ghost in self.ghosts:
            if (self.pacman.getCoord() == ghost.get_coord()):
                self.pacmanCaught = True

    def reset_ghosts(self):
        for ghost in self.ghosts:
            ghost.reset_character()
        # self.pacman.reset_character()

    """"Getters"""

    # Getter: returns dictionary, Coordinate mapped on a Candy object
    def get_candy_dict(self):
        return self.candies

    # Getter: returns max amount of colums and rows
    def get_max(self):
        return self.map.tiles_horiz_size - 1, self.map.tiles_vert_size - 1

    def get_pacman_coord(self):
        return self.pacman.getCoord()

    def get_gates(self):
        return self.map.get_gates()

    """"Events"""

    def check_quit_events(self):
        for event in pg.event.get(pg.QUIT):
            self.gameExit = True

    def check_move_events(self):
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

    def check_x_event(self):
        for event in pg.event.get(pg.KEYDOWN):
            if event.key == pg.K_x:
                self.gamemode = 2

    """"Main method"""

    # This is the main method
    # It catches every input from the keyboard
    # Also it functions as a kind of timeline everything in the while loop will be exectued as long as the game hasn't stopped
    def run(self):
        while not self.gameExit:
            # If the game is not paused, the game wil continue
            if not (self.pauze):
                self.gamemode_handler()
                # The event queue will block due to too much keyboard input(pygame issue). This code prevents the event queue from blocking
                pg.event.set_allowed(pg.KEYDOWN)
                pg.event.set_allowed(pg.QUIT)
            else:
                for event in pg.event.get(pg.KEYDOWN):
                    # Pauze button: p
                    if event.key == pg.K_p:
                        self.pauze = False
            self.check_quit_events()

        pg.quit()
        quit()


game = Game()
game.run()
