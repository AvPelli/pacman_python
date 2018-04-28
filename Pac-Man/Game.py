from copy import deepcopy

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
        self.__game_display = pg.display.set_mode(resolution)
        self.__init_game()

    # Initialise the game. It can also be used to reset the game!
    def __init_game(self):
        self.__gamemode = 1
        self.__pauze = False
        self.__game_exit = False
        self.__pacman_caught = False
        self.__ghost_caught = False
        self.__next = False

        self.start_time_scatter = pg.time.get_ticks()
        self.scatter_timer = 0

        self.start_time_frightened = 0
        self.frightened_timer = 0
        self.frightened_mode = False

        # Music settings
        self.__intro_played = False

        # Startscreen settings
        self.__mainmenu_exit = False

        # Game objects
        self.__map = Map(self, resolution[0], resolution[1], tile_size)
        self.clock = pg.time.Clock()
        self.__candies = self.__map.get_candy_dict()
        self.__pacman = PacMan(self.__map.get_pacman_start(), self, self.__map.get_coord_dict())

        self.__ghosts = []
        starting_positions = self.__map.get_ghosts_start()
        for i in starting_positions:
            self.__ghosts.append(Ghost(i, self, self.__map.get_coord_dict()))

        # Link objects
        self.__map.set_pacman(self.__pacman)

    def __gamemode_handler(self):
        if self.__gamemode == 1:
            self.__start_screen()
        elif self.__gamemode == 2:
            self.__ready_screen()
        elif self.__gamemode == 3:
            self.clock.tick()  # start the game timer (to measure time for scatter/chase mode)
            self.__play_screen()
        elif self.__gamemode == 4:
            self.__reset_screen()
        elif self.__gamemode == 5:
            self.__gameover_screen()
        elif self.__gamemode == 6:
            self.__gameover_screen(wait=True) # Make the game wait for an event
        elif self.__gamemode == 7:
            self.__game_won()

    # Startscreen mode - game displays startscreen
    def __start_screen(self):
        startscreen_image = pg.image.load("res/startscreen/startscreen.jpg")
        self.__game_display.blit(startscreen_image, (0, 125))
        # Print highscore on the screen
        score = self.__read_highscores()
        if(score != 0):
            for i in range(len(score)):
                text=score[i].strip()
                self.__map.draw_text(text,12+(4-len(text)),21+i,(150,50,150))
        pg.display.flip()

        self.clock.tick(3)

        # Event check, quit event check first
        self.__check_x_event()
        self.__check_quit_events()

    # Setting up the game - press a  KEY to start
    def __ready_screen(self):
        # Draw methods, be aware of the sequence!
        self.__map.draw_candy()
        self.__map.draw_startpacman(self.__map.get_pacman_start())
        self.__map.draw_text("READY!", 11, 20, (255, 238, 0))
        score=self.__read_highscores()
        if len(score) != 0:
            self.__map.draw_text(score[0], 11, 1)
        self.__map.draw_oneup()
        pg.display.update()
        self.clock.tick(50)

        # Music methods
        if not (self.__intro_played):
            self.SONG_END = pg.USEREVENT + 1
            pg.mixer.music.set_endevent(self.SONG_END)
            pg.mixer.music.load("res/files/music/pacman-beginning/pacman_beginning.wav")
            pg.mixer.music.play()
            self.__intro_played = True
        # Event check, quit event check first
        self.__check_quit_events()
        self.__check_beginningmusic_events()

    # Gaming
    def __play_screen(self):
        self.__game_display.fill(black)
        self.__map.draw_candy()
        score=self.__read_highscores()
        if len(score) != 0:
            self.__map.draw_text(score[0], 11, 1)

        if not self.__ghost_caught:
            self.__pacman.move()

        if self.__pacman.is_super_candy_eaten():

            # Start frightened timer
            self.start_time_frightened = pg.time.get_ticks()

            for ghost in self.__ghosts:
                # set_frightened() to display blue (frightened) ghosts
                self.frightened_mode = True
                ghost.set_frightened(True)
                ghost.frightened()

            # Reset to False, this if-block only has to be run once every supercandy
            self.__pacman.supercandy_eaten = False

        # Frightened_mode = False : ghosts use move() and scatter()
        if not self.frightened_mode:
            # Count time for scatter mode
            self.scatter_timer = pg.time.get_ticks() - self.start_time_scatter
            self.check_pacman_caught()

            # Scatter 7 seconds
            if (self.scatter_timer < 20000):
                for ghost in self.__ghosts:
                    ghost.scatter()

            # Chase 20 seconds
            elif (self.scatter_timer < 27000):
                for ghost in self.__ghosts:
                    ghost.move()

            else:
                # Reset timer
                self.start_time_scatter = pg.time.get_ticks()

        # Frightened_mode = True : ghosts use frightened()
        else:
            self.frightened_timer = pg.time.get_ticks() - self.start_time_frightened
            self.check_ghost_caught()

            if (self.frightened_timer < 5000):
                for ghost in self.__ghosts:
                    if ghost.get_gostart():
                        ghost.move_to_start()
                    else:
                        ghost.frightened()

            else:
                self.frightened_mode = False
                for ghost in self.__ghosts:
                    ghost.set_frightened(False)
                    ghost.imagechooser()

        self.__map.draw_oneup()
        self.clock.tick(60)
        pg.display.update()
        self.__play_background_music()

        # Event check, quit event check first
        self.__check_move_events()
        self.__check_quit_events()

        if (self.__pacman_caught):
            pg.mixer.Channel(0).stop()
            lifes = self.__pacman.get_lifes() - 1
            self.__pacman.set_lifes(lifes)
            self.__pacman_caught = False
            self.__gamemode = 4  # reset the game: ghosts in center and pacman in middle
            # each time pac-man gets caught,this song will be played if he has no lifes anymore this somng will play in game_over_screen
            if (self.__pacman.get_lifes()):
                pg.mixer.music.load("res/files/music/pacman-death/pacman_death.wav")
                pg.mixer.music.play()

        if not (self.__pacman.get_lifes()):
            self.__gamemode = 5  # no more lifes left: game over

        if (len(self.__candies) == 0):
           self.__gamemode = 7

        if self.__next:  # Only possible in the next loop
            print(self.__next, print("next"))
            for ghost in self.__ghosts:
                ghost.set_eaten(False)  # Ghosts eaten -> false, ghost not eaten -> still false
            self.__next = False

        if (self.__ghost_caught):
            print(self.__ghost_caught, "ghost caught")
            self.__ghost_caught = False
            self.__pacman.set_streak(1)
            self.__next = True
            pg.time.delay(1000)

    def __reset_screen(self):
        pg.time.delay(1000)  # wait 1 second

        # pacman back to the starting position
        self.__pacman.reset_character()

        # ghosts back to starting position
        self.reset_ghosts()
        self.__gamemode = 3

    def __gameover_screen(self,wait=False):
        if not wait:
           pg.time.delay(1000)
           self.__game_display.fill(black)
           self.__map.draw_candy()
           self.__map.draw_oneup()
           pg.display.update()
           deathco = self.__pacman.get_coord()
           pg.mixer.music.load("res/files/music/pacman-death/pacman_death.wav")
           pg.mixer.music.play()
           self.__map.draw_pacmandeathani(deathco)
           pg.display.update()
           self.__gamemode = 6
        else:
           pg.time.delay(1000)
           self.__game_display.fill(black)
           self.__map.change_wall_color()
           self.__map.draw_map()
           self.__map.draw_text("LOSER!", 11, 14, (255, 238, 0))
           self.__map.draw_text("PRESS X TO RESTART GAME", 3, 17, (255, 0, 0))
           pg.display.update()
           pg.time.delay(1000)
           self.__map.change_wall_color(won=False)
           self.__map.draw_map()
           self.__map.draw_text("LOSER!", 11, 14, (255, 238, 0))
           pg.display.update()
           self.__check_x_event(reset=True)

        # Event check, quit event check first
        self.__save_highscore()
        score = self.__read_highscores()
        if len(score) != 0:
            self.__map.draw_text(score[0], 11, 1)
            pg.display.update()
        self.__check_quit_events()

    def __game_won(self):
        self.__save_highscore()
        score = self.__read_highscores()
        if len(score) != 0:
            self.__map.draw_text(score[0], 11, 1)
            pg.display.update()

        pg.time.delay(1000)
        self.__game_display.fill(black)
        self.__map.change_wall_color()
        self.__map.draw_map()
        self.__map.draw_text("YOU HAVE WON!", 8, 14, (255, 238, 0))
        self.__map.draw_text("PRESS X TO RESTART GAME", 3, 17, (255,0, 0))
        pg.display.update()
        pg.time.delay(1000)
        self.__map.change_wall_color(won=False)
        self.__map.draw_map()
        self.__map.draw_text("YOU HAVE WON!", 8, 14, (255, 238, 0))
        pg.display.update()

        self.__check_x_event(reset=True)
        self.__check_quit_events()


    def check_pacman_caught(self):
        for ghost in self.__ghosts:
            if self.__pacman.get_coord() == ghost.get_coord():
                self.__pacman_caught = True

    # Pacman searches for ghosts
    def check_ghost_caught(self):
        for ghost in self.__ghosts:
            if self.__pacman.get_coord() == ghost.get_coord():
                if not ghost.get_gostart():
                    self.__ghost_caught = True
                    # Make the ghost start moving to the center
                    ghost.set_gostart(True)

    def reset_ghosts(self):
        for ghost in self.__ghosts:
            ghost.reset_character()
        # self.__pacman.reset_character()

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
        new_score = []  # This list keeps the top max_count new high scores. It cannot be higher than max_count
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

    def __play_background_music(self):
        if not pg.mixer.Channel(0).get_busy():
            pg.mixer.Channel(0).play(pg.mixer.Sound("res/files/music/pacman-siren/Pacman_Siren.wav"))

    """"Getters"""

    def get_game_display(self):
        return self.__game_display

    # Getter: returns max amount of colums and rows
    def get_max(self):
        return self.__map.get_tiles_horiz_size() - 1, self.__map.get_tiles_vert_size() - 1

    # Getters: return map
    def get_map(self):
        return self.__map

    def get_pacman(self):
        return self.__pacman

    def get_pacman_coord(self):
        return deepcopy(self.__pacman.get_coord())

    def get_pacman_direction(self):
        return deepcopy(self.__pacman.get_direction())

    def get_pacman_direction(self):
        return deepcopy(self.__pacman.get_direction())

    def get_ghosts(self):
        return self.__ghosts

    """"Events"""

    def __check_quit_events(self):
        for event in pg.event.get(pg.QUIT):
            self.__game_exit = True

    def __check_move_events(self):
        for event in pg.event.get(pg.KEYDOWN):
            # Pauze button: p
            if event.key == pg.K_p:
                self.__pauze = True if self.__pauze == False else False
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
            self.__map.draw_text('', 11, 20)

    def __check_x_event(self,reset=False):
        for event in pg.event.get(pg.KEYDOWN):
            if event.key == pg.K_x:
                if not reset:
                   self.__gamemode = 2
                else:
                   self.__game_display.fill(black)
                   pg.display.update()
                   self.__init_game()

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
