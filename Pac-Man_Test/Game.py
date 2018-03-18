import pygame

from Coordinate import Coordinate
from Direction import Direction
from PacMan import PacMan


class Game:
    def __init__(self):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("PacMan")
        self.clock = pygame.time.Clock()
        self.pacman = PacMan(self.gameDisplay, Coordinate(5, 5))

    def reDraw(self):
        white = (255, 255, 255)
        black = (0, 0, 0)
        self.gameDisplay.fill(black)
        self.pacman.move()
        pygame.display.update()
        self.clock.tick(5)

    def run(self):
        gameExit = False

        while not gameExit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.pacman.setDirection(Direction.LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.pacman.setDirection(Direction.RIGHT)
                    elif event.key == pygame.K_UP:
                        self.pacman.setDirection(Direction.UP)
                    elif event.key == pygame.K_DOWN:
                        self.pacman.setDirection(Direction.DOWN)
            self.reDraw()

        pygame.quit()
        quit()


game = Game()
game.run()
