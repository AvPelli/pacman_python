import pygame as pg


class Fruit:
    def __init__(self, game_Display, coordinate, fruitselector, fruittype):
        self.__game_Display = game_Display
        self.__image = pg.image.load("res/fruit/" + fruittype + ".png")
        self.__coordinate = coordinate
        self.__fruittype = fruittype
        self._fruitselector = fruitselector
        self.__bonus = self._fruitselector.get_fruitbonus(self.__fruittype)
        self.__eaten = False

    def draw(self):
        coord_pixels = self.__coordinate.get_pixel_tuple()
        res = coord_pixels[0] + 8, coord_pixels[1]
        self.__game_Display.blit(self.__image, res)

    def get_fruit_name(self):
        return self.__fruittype

    def get_score(self):
        if not self.__eaten:
            self.__eaten = True
            return self.__bonus
        else:
            return 0

    def get_eaten(self):
        return self.__eaten
