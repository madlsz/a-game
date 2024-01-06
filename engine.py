import pygame
import numpy as np

from van_gogh import VanGogh
from game import Game
import tetrominos


class Engine:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((400, 800))
        self.gogh = VanGogh(self.screen)
        self.game = Game()
        self.fps = 30
        self.gravity_time = None
        self.movement_time = None
        self.running = True


    def start(self):
        self.game.spawn_tetromino(tetrominos.create_instance("I"))
        print(self.game)

        self.gravity_time = pygame.time.get_ticks()
        self.movement_time = pygame.time.get_ticks()

        while self.running:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()

            self.gogh.draw(self.game.board)

        pygame.quit()