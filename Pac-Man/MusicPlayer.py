import pygame as pg


class MusicPlayer():

    def __init__(self, path="res/files/music/"):
        self.__path = path

    def play_music(self, specific_path):
        pg.mixer.music.load(self.__path + specific_path)
        pg.mixer.music.play()

    def play_background_music(self):
        if not pg.mixer.Channel(0).get_busy():
            pg.mixer.Channel(0).play(pg.mixer.Sound("res/files/music/pacman-siren/Pacman_Siren.wav"))
