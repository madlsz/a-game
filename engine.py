import pygame
# import numpy as np

from van_gogh import VanGogh
from game import Game
# import tetrominos


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


    def gravity(self, keys):
        if keys[pygame.K_DOWN]:
            self.gravity_time_timeout = 100
        else:
            self.gravity_time_timeout = 600
        elapsed_time = pygame.time.get_ticks() - self.gravity_time
        if elapsed_time >= self.gravity_time_timeout:
            self.gravity_time = pygame.time.get_ticks()
            self.game.clear_active()
            self.game.move_tetromino_down()
            print(self.game)
            print(f"width:{self.game.current_tetromino.width}, height:{self.game.current_tetromino.height}")
            print(f"x:{self.game.current_tetromino.x}, y:{self.game.current_tetromino.y}")

    
    def horizontal_movement(self, keys):
        if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
            elapsed_time = pygame.time.get_ticks() - self.movement_time
            if elapsed_time >= self.movement_time_timeout:
                self.movement_time = pygame.time.get_ticks()
                self.game.clear_active()
                if keys[pygame.K_LEFT]:
                    self.game.move_tetromino_left()
                elif keys[pygame.K_RIGHT]:
                    self.game.move_tetromino_right()

    
    def rotations(self, keys):
        if keys[pygame.K_UP]:
            elapsed_time = pygame.time.get_ticks() - self.rotation_time
            if elapsed_time >= self.rotation_time_timeout:
                self.rotation_time = pygame.time.get_ticks()
                self.game.clear_active()
                self.game.rotate_tetromino()


    def start(self):
        self.game.spawn_tetromino("I")

        self.gravity_time = pygame.time.get_ticks()
        self.movement_time = pygame.time.get_ticks()
        self.rotation_time = pygame.time.get_ticks()

        while self.running:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            self.gravity(keys)
            self.horizontal_movement(keys)
            self.rotations(keys)
            self.gogh.draw(self.game.active, self.game.landed)

        pygame.quit()