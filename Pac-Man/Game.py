from copy import deepcopy

import pygame as pg  # Importeren van pg module
from Direction import Direction
from Ghost import Ghost
from Maze import Maze
from MusicPlayer import MusicPlayer
from PacMan import PacMan
from FruitSelector import FruitSelector

black = (0, 0, 0)
tile_size = 16
resolution = (448, 576)
clock = pg.time.Clock()


class Game():
    """
    Constructor of Game\n
    This class is the core of the game
    """

    def __init__(self):
        """
        Initialises the Pygame module and the pacman game
        """

        pg.init()
        pg.display.set_caption('Pac-Man')
        # Game variables
        self.__game_display = pg.display.set_mode(resolution)
        self.__won_counter = 0
        self.__init_game()

    def __init_game(self, old_score=0):
        """
        Initialise the game. It can also be used to reset the game!\n
        :param old_score: Remembers the old score of the past level\n
        :return: void
        """
        # when resetting the game, it is important to know if we have advanced to the next level or not (in that case,
        # the starting screen won't be shown). this is done by checking if we already have a score
        self.__gamemode = 1 if old_score == 0 else 2
        self.__pauze = False
        self.__game_exit = False
        self.__pacman_caught = False
        self.__ghost_caught = False
        self.__next = False


        self.__first_time_loop = True
        self.start_time_scatter = pg.time.get_ticks()
        self.scatter_timer = 0

        self.start_time_frightened = 0
        self.frightened_timer = 0
        self.frightened_mode = False

        # Music settings
        self.music_player = MusicPlayer()
        self.__intro_played = False

        # Startscreen settings
        self.__mainmenu_exit = False

        # Game objects
        self.__maze = Maze(self, resolution[0], resolution[1], tile_size)
        self.clock = pg.time.Clock()
        self.__candies = self.__maze.get_candy_dict()
        self.__pacman = PacMan(self, self.__maze.get_pacman_start(), self.__maze.get_coord_dict(), old_score)
        self.fruitselector = FruitSelector(self.__game_display, self, self.__won_counter)

        self.__ghosts = []
        starting_positions = self.__maze.get_ghosts_start()
        for i in starting_positions:
            self.__ghosts.append(Ghost(self, i, self.__maze.get_coord_dict()))

        # Link objects
        self.__maze.set_pacman(self.__pacman)
        # Score
        score = self.__read_highscores()
        if (len(score) != 0):
            self.__max_digits_score = len(score[0].strip())
        else:
            self.__max_digits_score = 0

    def __gamemode_handler(self):
        """
        Checks which game mode it needs to activate\n
        :return: void
        """
        if self.__gamemode == 1:
            self.__start_screen()
        elif self.__gamemode == 2:
            self.__ready_screen()
        elif self.__gamemode == 3:
            self.__play_screen()
        elif self.__gamemode == 4:
            self.__reset_screen()
        elif self.__gamemode == 5:
            self.__gameover_screen()
        elif self.__gamemode == 6:
            self.__gameover_screen(wait=True)  # Make the game wait for an event
        elif self.__gamemode == 7:
            self.__game_won()

    def __start_screen(self):
        """
        Startscreen mode - game displays startscreen\n
        :return: void
        """
        startscreen_image = pg.image.load("res/startscreen/startscreen.jpg")
        self.__game_display.blit(startscreen_image, (0, 125))
        # Print highscore on the screen
        score = self.__read_highscores()
        if (score != 0):
            for i in range(len(score)):
                text = score[i].strip()
                self.__maze.draw_text(text, 12 + (self.__max_digits_score - len(text)), 21 + i, (150, 50, 150))
        pg.display.flip()

        self.clock.tick(3)

        # Event check, quit event check first
        self.__check_x_event()
        self.__check_quit_events()

    def __ready_screen(self):
        """
        Setting up the game - press a  KEY to start\n
        :return: void
        """
        # Draw methods, be aware of the sequence!
        self.__maze.draw_mapwithcandy()
        self.__pacman.draw_startpacman()
        self.__maze.draw_text("READY!", 11, 20, (255, 238, 0))
        self.__maze.draw_todisplay()

        self.clock.tick(60)

        # Music methods
        if not (self.__intro_played):
            self.SONG_END = pg.USEREVENT + 1
            pg.mixer.music.set_endevent(self.SONG_END)
            self.music_player.play_music("pacman-beginning/pacman_beginning.wav")
            self.__intro_played = True

        # Event check, quit event check first
        self.__check_quit_events()
        self.__check_beginningmusic_events()

    # Gaming
    def __play_screen(self):
        """
        The playing screen.\n
        :return: void
        """
        self.__game_display.fill(black)
        self.__maze.draw_candy()
        self.draw_score()

        self.fruitselector.calc_until_fruit()
        self.__pacman.move()

        if self.__pacman.is_super_candy_eaten():
            for ghost in self.__ghosts:
                ghost.start_timer_frightend()
            # Reset to False, this if-block only has to be run once every supercandy
            self.__pacman.supercandy_eaten = False

        for ghost in self.__ghosts:
            ghost.move_selector()

        self.__maze.draw_oneup()

        self.clock.tick(50)
        pg.display.update()
        self.music_player.play_background_music()

        # Event check, quit event check first
        self.__check_move_events()
        self.__check_quit_events()

        if (self.__pacman_caught):
            self.__pacman.decrease_lifes()
            self.__pacman_caught = False

        if len(self.__candies) == 0:
            self.__gamemode = 7

        if self.__ghost_caught:
            self.__ghost_caught = False
            self.__maze.draw_candy()
            pg.display.update()
            pg.time.delay(1000)

    def reset_pacman_streak(self):
        """
        Resets pac-man's score\n
        :return:  void
        """
        self.__pacman.reset_streak()

    def draw_pacman_death(self, coord):
        """
        When pac-man dies, it will display a dead animation\n
        :param coord: type Coordinate\n
        :return: void
        """
        self.__maze.draw_pacmandeathani(coord)

    def get_candy_amount(self):
        """
         Getter\n
         :return: int
        """
        return self.__maze.get_candy_amount()

    def __reset_screen(self):
        """
        :return: void
        """
        pg.time.delay(1000)  # wait 1 second

        # pacman back to the starting position
        self.__pacman.reset_character()

        # ghosts back to starting position
        self.reset_ghosts()
        self.__gamemode = 3

    def __gameover_screen(self, wait=False):
        """
        When pac-man loses all his lifes, the game will be over.\n
        :param wait: By default False\n
        :return: void
        """
        self.music_player.stop_background_music();
        if not wait:
            pg.time.delay(1000)
            self.__game_display.fill(black)
            self.__maze.draw_candy()
            self.__maze.draw_oneup()
            pg.display.update()
            deathco = self.__pacman.get_coord()
            self.music_player.play_music("pacman-death/pacman_death.wav")

            self.__maze.draw_pacmandeathani(deathco)
            pg.display.update()
            self.__gamemode = 6
            self.__save_highscore()
        else:
            score = self.__read_highscores()
            if len(score) != 0:
                self.__maze.draw_text(score[0], 11, 1)
                pg.display.update()
            pg.time.delay(500)
            self.__game_display.fill(black)
            self.__maze.change_wall_color()
            self.__maze.draw_map()
            self.__maze.draw_text("LOSER!", 11, 14, (255, 238, 0))
            self.__maze.draw_text("PRESS X TO RESTART GAME", 3, 17, (255, 0, 0))
            pg.display.update()
            pg.time.delay(500)
            self.__maze.change_wall_color(won=False)
            self.__maze.draw_map()
            self.__maze.draw_text("LOSER!", 11, 14, (255, 238, 0))
            pg.display.update()
            self.__check_x_event(reset=True)

        # Event check, quit event check first
        self.__check_quit_events()

    def set_gamemode(self, waarde):
        """
         Choose a game mode\n
        :param waarde: type: int
        :return: void
        """
        self.__gamemode = waarde

    def __game_won(self):
        """
        The winning screen\n
        :return: void
        """
        self.__save_highscore()
        score = self.__read_highscores()
        if len(score) != 0:
            self.__maze.draw_text(score[0], 11, 1)
            pg.display.update()

        pg.time.delay(1000)
        self.__game_display.fill(black)
        self.__maze.change_wall_color()
        self.__maze.draw_map()
        self.__maze.draw_text("YOU HAVE WON!", 8, 14, (255, 238, 0))
        self.__maze.draw_text("PRESS X TO RESTART GAME", 3, 17, (255, 0, 0))
        pg.display.update()
        pg.time.delay(1000)
        self.__maze.change_wall_color(won=False)
        self.__maze.draw_map()
        self.__maze.draw_text("YOU HAVE WON!", 8, 14, (255, 238, 0))
        pg.display.update()

        self.__check_x_event(reset=True, won=True)
        self.__check_quit_events()

    def reset_ghosts(self):
        for ghost in self.__ghosts:
            ghost.reset_character()

    def update_fruit_selector(self):
        self.fruitselector.update_candies_active()

    def __save_highscore(self):
        score = []
        score.append(self.__pacman.get_score())
        filename = "res/files/highscore.txt"
        try:
            for line in open(filename, "r"):
                try:
                    score.append(int(line.strip()))
                except:
                    pass
        except:
            print("Creating new highscore file...")
        score.sort()
        score.reverse()
        new_score = []  # This list keeps the top max_count new high scores. It cannot be higher than max_amount
        max_amount = 5
        if len(score) < 5:
            max_amount = len(score)
        for i in range(max_amount):
            new_score.append(str(score[i]))

        file = open(filename, "w+")
        file.write("\n".join(new_score))
        file.close()

    def __read_highscores(self):
        scores = []
        filename = "res/files/highscore.txt"
        for line in open(filename, "r"):
            scores.append(line)
        return scores

    def __reset_highscore(self):
        filename = "res/files/highscore.txt"
        open(filename, "w")

    """"Getters"""

    def get_game_display(self):
        return self.__game_display

    # Getter: returns max amount of colums and rows
    def get_max(self):
        return self.__maze.get_tiles_horiz_size() - 1, self.__maze.get_tiles_vert_size() - 1

    # Getters: return map
    def get_map(self):
        return self.__maze

    def get_pacman(self):
        return self.__pacman

    def get_pacman_coord(self):
        return deepcopy(self.__pacman.get_coord())

    def get_pacman_direction(self):
        return deepcopy(self.__pacman.get_direction())

    def get_ghosts(self):
        return self.__ghosts

    def get_fruit_selector(self):
        return self.fruitselector

    """"Events"""

    def __check_quit_events(self):
        for event in pg.event.get(pg.QUIT):
            self.__game_exit = True

    def __check_move_events(self):
        for event in pg.event.get(pg.KEYDOWN):
            # Pauze button: p
            if event.key == pg.K_p:
                self.__pauze = True if self.__pauze == False else False
                pg.mixer.Channel(0).stop()
            # Sends the direction input to Pacman
            elif event.key == pg.K_LEFT:
                self.__pacman.set_direction(Direction.LEFT)
            elif event.key == pg.K_RIGHT:
                self.__pacman.set_direction(Direction.RIGHT)
            elif event.key == pg.K_UP:
                self.__pacman.set_direction(Direction.UP)
            elif event.key == pg.K_DOWN:
                self.__pacman.set_direction(Direction.DOWN)

    def __check_beginningmusic_events(self):
        for event in pg.event.get(self.SONG_END):
            self.__gamemode = 3
            self.__maze.draw_text('', 11, 20)

    def __check_x_event(self, reset=False, won=False):
        for event in pg.event.get(pg.KEYDOWN):
            if event.key == pg.K_x:
                if not reset:
                    self.__gamemode = 2
                else:
                    self.__game_display.fill(black)
                    pg.display.update()
                    if won:
                        self.__won_counter += 1
                        self.__init_game(self.__pacman.get_score())
                    else:
                        self.__init_game()

    # Setters that act like events, are triggered in other classes
    def set_pacman_caught(self):
        self.__pacman_caught = True

    def set_ghost_caught(self):
        self.__pacman.set_streak(1)  # adds 1 to the streak
        self.__ghost_caught = True

    def draw_score(self):
        score = self.__read_highscores()
        if len(score) != 0:
            self.__maze.draw_text(score[0], 11, 1)

    """"Main method"""

    # This is the main method
    # It catches every input from the keyboard
    # Also it functions as a kind of timeline everything in the while loop will be exectued as long as the game hasn't stopped
    def run(self):
        while not self.__game_exit:
            # If the game is not paused, the game wil continue
            if not (self.__pauze):
                self.__gamemode_handler()
                # The event queue will block due to too much keyboard input(pygame issue). This code prevents the event queue from blocking
                pg.event.set_allowed(pg.KEYDOWN)
                pg.event.set_allowed(pg.QUIT)
            else:
                for event in pg.event.get(pg.KEYDOWN):
                    # Pauze button: p
                    if event.key == pg.K_p:
                        self.__pauze = False
            self.__check_quit_events()

        pg.quit()
        quit()


game = Game()
game.run()
