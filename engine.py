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
        self.gravity_time_timeout = 600
        self.movement_time = None
        self.movement_time_timeout = 50
        self.rotation_time = None
        self.rotation_time_timeout = 50
        self.running = True


    def start(self):
        self.game.spawn_tetromino(tetrominos.create_instance("T"))

        self.gravity_time = pygame.time.get_ticks()
        self.movement_time = pygame.time.get_ticks()
        self.rotation_time = pygame.time.get_ticks()

        while self.running:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            elapsed_time = pygame.time.get_ticks() - self.gravity_time
            if elapsed_time >= self.gravity_time_timeout:
                self.gravity_time = pygame.time.get_ticks()
                if keys[pygame.K_DOWN]:
                    self.gravity_time_timeout = 100
                else:
                    self.gravity_time_timeout = 600
                self.game.clear_board()
                self.game.move_tetromino_down()

            elapsed_time = pygame.time.get_ticks() - self.movement_time
            if elapsed_time >= self.movement_time_timeout:
                self.movement_time = pygame.time.get_ticks()
                if keys[pygame.K_RIGHT]:
                    self.game.clear_board()
                    self.game.move_tetromino_right()
                elif keys[pygame.K_LEFT]:
                    self.game.clear_board()
                    self.game.move_tetromino_left()

            elapsed_time = pygame.time.get_ticks() - self.rotation_time
            if elapsed_time >= self.rotation_time_timeout:
                self.rotation_time = pygame.time.get_ticks()
                if keys[pygame.K_UP]:
                    self.game.clear_board()
                    self.game.rotate_tetromino()


            self.gogh.draw(self.game.board)

        pygame.quit()