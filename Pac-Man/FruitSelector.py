from Coordinate import Coordinate
from Fruit import Fruit


class FruitSelector:
    fruit_location = Coordinate(13, 17)

    def __init__(self, game_display, game, won_counter):
        self._game_Display = game_display
        self.__game = game
        self.__names = {"Cherry": 60, "Apple": 90, "Strawberry": 120, "Orange": 150, "Green Melon": 180}
        self.__images = {}
        # self.__fruitcoord = Coordinate(232, 320)
        self.__level = 1
        # self.__starttimer = pg.time.get_ticks()
        self.__time = 0
        self.reset_per_level(won_counter)

    # nog self.__fruits aanpassen per lvl
    def reset_per_level(self, level=0):
        self.__candies_left = self.__game.get_map().get_candy_amount()
        self.__fruits = (Fruit(self._game_Display, FruitSelector.fruit_location, self, "Cherry"),
                         Fruit(self._game_Display, FruitSelector.fruit_location, self, "Cherry"))

    def calc_until_fruit(self, level=0):
        self.__level = level
        if 180 > self.__candies_left > 140 and not self.__fruits[0].get_eaten():
            self.__fruits[0].draw()
        elif 60 < self.__candies_left < 100 and not self.__fruits[1].get_eaten():
            self.__fruits[1].draw()

    def get_fruitbonus(self, fruitname):
        return self.__names[fruitname]

    def get_score(self):
        if 180 > self.__candies_left > 140:
            return self.__fruits[0].get_score()
        elif 60 < self.__candies_left < 100:
            return self.__fruits[1].get_score()
        return 0

    def fruit_active(self):
        return (180 > self.__candies_left > 140 and not self.__fruits[0].get_eaten()) \
               or (60 < self.__candies_left < 100 and not self.__fruits[1].get_eaten())

    def update_candies_active(self):
        self.__candies_left -= 1

    def get_fruit_coord_tuple(self):
        return FruitSelector.fruit_location.get_x(), FruitSelector.fruit_location.get_y()
