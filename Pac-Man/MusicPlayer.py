import pygame as pg


class MusicPlayer:

    def __init__(self, path="res/files/music/"):
        """
        Creates a MusicPlayer, which is used by the game to play sounds.\n
        :param path: The standard path where music files have to be located within the project folder.\n
        """
        self.__path = path

    def play_music(self, specific_path):
        """
        To play a sound, the file has to be located within the __path folder in order to be played.\n
        :param specific_path: the files' name
        :return: void
        """
        pg.mixer.music.load(self.__path + specific_path)
        pg.mixer.music.play()

    def play_background_music(self):
        """
        To play the standard background music of the game.\n
        :return: void
        """
        if not pg.mixer.Channel(0).get_busy():
            pg.mixer.Channel(0).play(pg.mixer.Sound("res/files/music/pacman-siren/Pacman_Siren.wav"))

    def stop_background_music(self):
        """
        To temporally stop the background music, used when Pacman has been eaten by a ghost.\n
        :return: void
        """
        pg.mixer.Channel(0).stop()
