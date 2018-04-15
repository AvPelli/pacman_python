import pygame as pg

import Game

game_display = pg.display.set_mode(Game.resolution)
pg.display.set_caption('Pac-Man')
clock = pg.time.Clock()


class StartScreen():

    def __init__(self):
        self.game_display = game_display  # The display of the game
        self.__width = Game.width
        self.__height = Game.height
        self.clock = pg.time.Clock()
        filename = "res/files/hiscores.txt"
        imagefile = "res/startscreen/startscreen.jpg"

        self.startscreen_image = pg.image.load(imagefile)
        self.game_display.fill(Game.black)

    # Redraw Startscreen for animation:
    def redraw(self):
        self.game_display.blit(self.startscreen_image, (0, 125))
        pg.display.flip()

        self.clock.tick(10)

    def run(self):
        mainmenuExit = False
        gameExit = False

        while not mainmenuExit:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    gameExit = True
                    mainmenuExit = True

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_x:
                        mainmenuExit = True

            self.redraw()

        # Free resources used by mainmenu screen:
        pg.quit()
        # Let the game start if the player don't press Quit
        if not gameExit:
            game = Game.Game()
            game.run()


startscreen = StartScreen()
startscreen.run()
