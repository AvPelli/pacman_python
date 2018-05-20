#in Klasse Game
def draw_target_tile(self):
        blinky = self.__ghosts[0]
        target_coord = blinky.get_target_tile()
        image = pg.image.load("res/tileset/DoelTegel/Doel_rood.png")
        self.__game_display.blit(image, target_coord.get_pixel_tuple())

        pinky = self.__ghosts[1]
        target_coord = pinky.get_target_tile()
        image = pg.image.load("res/tileset/DoelTegel/Doel_roze.png")
        self.__game_display.blit(image, target_coord.get_pixel_tuple())

        inky = self.__ghosts[2]
        target_coord = inky.get_target_tile()
        image = pg.image.load("res/tileset/DoelTegel/Doel_blauw.png")
        self.__game_display.blit(image, target_coord.get_pixel_tuple())

        clyde = self.__ghosts[3]
        target_coord = clyde.get_target_tile()
        image = pg.image.load("res/tileset/DoelTegel/Doel_oranje.png")
        self.__game_display.blit(image, target_coord.get_pixel_tuple())

#in klasse ghost
def get_target_tile(self):
        return self.__target_tile

#in klasse ghost
tijd=str(int(self.scatter_timer/1000))
self._game.get_map().draw_text(tijd+' sec',22,1,(244,164,96))
self.__maze.draw_text("TIME",22,0,(255,105,180))

#in klasse game
def draw_circle(self):
    clyde = self.__ghosts[3]
    target_coord = clyde.get_target_tile()
    image = pg.image.load("res/tileset/DoelTegel/Doel_oranje.png")
    self.__game_display.blit(image, target_coord.get_pixel_tuple())

    pg.draw.circle(self.__game_display, (255, 165, 0), self.__pacman.get_coord().get_pixel_tuple(), 16 * 10, 1)

#in klasse game
 def draw_vector(self):

         blinky = self.__ghosts[0]

         pinky = self.__ghosts[1]
         target_coord = pinky.get_target_tile()
         image = pg.image.load("res/tileset/DoelTegel/Doel_roze.png")
         self.__game_display.blit(image, target_coord.get_pixel_tuple())

         inky = self.__ghosts[2]
         target_coord = inky.get_target_tile()
         image = pg.image.load("res/tileset/DoelTegel/Doel_blauw.png")
         self.__game_display.blit(image, target_coord.get_pixel_tuple())

         pg.draw.line(self.__game_display,(255,255,255),blinky.get_coord().get_pixel_tuple(),inky.get_coord().get_pixel_tuple())
