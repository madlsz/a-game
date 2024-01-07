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
        self.current_time = None
        self.pressed_keys = None


    def gravity(self):
        if self.pressed_keys[pygame.K_DOWN]:
            self.gravity_time_timeout = 100
        else:
            self.gravity_time_timeout = 600
        elapsed_time = self.current_time - self.gravity_time
        if elapsed_time >= self.gravity_time_timeout:
            if self.game.move_tetromino_down():
                self.gravity_time = self.current_time

    
    def horizontal_movement(self):
        if self.pressed_keys[pygame.K_RIGHT] or self.pressed_keys[pygame.K_LEFT]:
            elapsed_time = self.current_time - self.movement_time
            if elapsed_time >= self.movement_time_timeout:
                if self.pressed_keys[pygame.K_LEFT]:
                    if self.game.move_tetromino_left():
                        self.movement_time = self.current_time
                        print(f"x:{self.game.current_tetromino.x} y:{self.game.current_tetromino.y}")
                elif self.pressed_keys[pygame.K_RIGHT]:
                    if self.game.move_tetromino_right():
                        self.movement_time = self.current_time
                        print(f"x:{self.game.current_tetromino.x} y:{self.game.current_tetromino.y}")
    

    def rotations(self):
        if self.pressed_keys[pygame.K_UP]:
            elapsed_time = self.current_time - self.rotation_time
            if elapsed_time >= self.rotation_time_timeout:
                if self.game.rotate_tetromino():
                    self.rotation_time = self.current_time

    def start(self):
        self.game.spawn_tetromino("t")

        self.current_time = pygame.time.get_ticks()
        self.gravity_time = self.current_time
        self.movement_time = self.current_time
        self.rotation_time = self.current_time

        while self.running:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.current_time = pygame.time.get_ticks()
            self.pressed_keys = pygame.key.get_pressed()
            self.gravity()
            self.horizontal_movement()
            self.rotations()
            self.gogh.draw(self.game.active, self.game.landed)

        pygame.quit()
