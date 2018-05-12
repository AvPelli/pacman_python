from Coordinate import Coordinate
from Fruit import Fruit
import pygame as pg

class FruitSelector:
    fruit_location = Coordinate(13, 17)

    def __init__(self, game_display, game, won_counter):
        """
        Creates a FruitSelector. \n
        It's function is to determine which fruits it should draw during the current level. It also knows
        when exactly to draw these, and will draw which fruits are already eaten in the bottom right corner of the screen.
        :param game_display: The display to which the fruit object is drawn.
        :param game: The game that holds this FruitSelector, needed for communication
        :param won_counter: The current level, needed to know which fruits to draw
        """
        self._game_Display = game_display
        self.__game = game
        self.__names = {"Cherry": 200, "Apple": 400, "Strawberry": 600, "Orange": 800, "Green Melon": 1000}
        self.__images = {}
        self.__eaten_fruits = []
        # self.__fruitcoord = Coordinate(232, 320)
        self.__level = won_counter
        # self.__starttimer = pg.time.get_ticks()
        self.__time = 0
        self.reset_per_level(won_counter)

    # nog self.__fruits aanpassen per lvl
    def reset_per_level(self, level=0):
        """
        While not needed, this method helps separating some of the __init__code that has it's own specific function:
        Initializing the fruits to draw
        :param level: the current level
        :return: void
        """
        self.__candies_left = self.__game.get_map().get_candy_amount()
        if level == 0:
            self.__fruits = (Fruit(self._game_Display, FruitSelector.fruit_location, self, "Cherry"),
                             Fruit(self._game_Display, FruitSelector.fruit_location, self, "Apple"))
        elif level == 1:
            self.__fruits = (Fruit(self._game_Display, FruitSelector.fruit_location, self, "Strawberry"),
                             Fruit(self._game_Display, FruitSelector.fruit_location, self, "Orange"))
        else:
            self.__fruits = (Fruit(self._game_Display, FruitSelector.fruit_location, self, "Green Melon"),
                             Fruit(self._game_Display, FruitSelector.fruit_location, self, "Green Melon"))
    def calc_until_fruit(self):
        """
        This method draws a fruit to the display when specific conditions are met, it simulates a
        time frame in which Pacman can eat the fruit
        :return: void
        """
        if 180 > self.__candies_left > 140 and not self.__fruits[0].get_eaten():
            self.__fruits[0].draw()
        elif 60 < self.__candies_left < 100 and not self.__fruits[1].get_eaten():
            self.__fruits[1].draw()

    def get_fruitbonus(self, fruitname):
        """
        This method returns the amount of score a certain type of fruit awards when eaten, by looking its fruitname
        up in it's dictionary.
        :param fruitname: needed to determine how many points this fruit awards
        :return: int
        """
        return self.__names[fruitname]

    def get_score(self):
        """
        This method returns the score of the eaten fruit to Pacman itself, it calls the get_score() method of the fruits
        themselves, whic honly returns their true score once (before they are eaten)
        :return: int, the eaten fruit's score
        """
        if 180 > self.__candies_left > 140:
            self.add_eaten_fruit(self.__fruits[0])
            return self.__fruits[0].get_score()
        elif 60 < self.__candies_left < 100:
            self.add_eaten_fruit(self.__fruits[1])
            return self.__fruits[1].get_score()
        return 0

    def fruit_active(self):
        """
        This method checks if a fruit is currently active(~ drawn) on the map, which
        is used by Pacman for collision detection
        :return: boolean
        """
        return (180 > self.__candies_left > 140 and not self.__fruits[0].get_eaten()) \
               or (60 < self.__candies_left < 100 and not self.__fruits[1].get_eaten())

    def update_candies_active(self):
        """
        This method substracts 1 from the active candy amount, is called whenenver pacman eats a candy. This variable
        is very important for the FruitSelector, it determines when any fruit will be drawn.
        :return: void
        """
        self.__candies_left -= 1

    def get_fruit_coord_tuple(self):
        """
        This method returns the fruit location, where it will be drawn
        :return: tuple with coordinates (x,y)
        """
        return FruitSelector.fruit_location.get_x(), FruitSelector.fruit_location.get_y()

    def draw_eaten_fruits(self):
        """
        This method draws the, so far, eaten fruits from this level
        :return: void
        """
        startpix = (384, 544)
        i = 0
        for fruit in self.__eaten_fruits:
            drawpix = startpix[0] + 32*i, startpix[1]
            i += 1
            self._game_Display.blit(fruit, drawpix)

    def add_eaten_fruit(self, fruit):
        """
        This method adds a fruit to the eaten_fruit list, so it will be drawn from now on
        :param fruit: the eaten fruit
        :return: void
        """
        fruitimg = pg.image.load("res/fruit/" + fruit.get_fruit_name() + "2.png")
        self.__eaten_fruits.append(fruitimg)