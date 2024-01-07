import pygame
import random

from van_gogh import VanGogh
from game import Game


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
        self.rotation_time_timeout = 75
        self.running = True
        self.current_time = None
        self.pressed_keys = None
        self.tetromino_types = ["j", "l", "s", "t", "z", "o", "i"]
        self.tetromino_counter = 0


    def tetrominos_bag(self):
        if self.tetromino_counter == len(self.tetromino_types):
            self.tetromino_counter = 0
            random.shuffle(self.tetromino_types)
        tetromino_type = self.tetromino_types[self.tetromino_counter]
        self.tetromino_counter += 1
        return tetromino_type


    def gravity(self):
        if self.pressed_keys[pygame.K_DOWN]:
            self.gravity_time_timeout = 100
        else:
            self.gravity_time_timeout = 600
        elapsed_time = self.current_time - self.gravity_time
        if elapsed_time >= self.gravity_time_timeout:
            if self.game.move_tetromino_down():
                self.gravity_time = self.current_time
            else:
                self.game.push_to_landed()
                if not self.game.spawn_tetromino(self.tetrominos_bag(), 4, 1):
                    self.running = False
                    print("Game over!")


    def horizontal_movement(self):
        if self.pressed_keys[pygame.K_RIGHT] or self.pressed_keys[pygame.K_LEFT]:
            elapsed_time = self.current_time - self.movement_time
            if elapsed_time >= self.movement_time_timeout:
                if self.pressed_keys[pygame.K_LEFT]:
                    if self.game.move_tetromino_left():
                        self.movement_time = self.current_time
                elif self.pressed_keys[pygame.K_RIGHT]:
                    if self.game.move_tetromino_right():
                        self.movement_time = self.current_time
    

    def rotations(self):
        if self.pressed_keys[pygame.K_UP]:
            elapsed_time = self.current_time - self.rotation_time
            if elapsed_time >= self.rotation_time_timeout:
                if self.game.rotate_tetromino():
                    self.rotation_time = self.current_time


    def start(self):
        self.game.spawn_tetromino(self.tetrominos_bag(), 4, 1)

        self.current_time = pygame.time.get_ticks()
        self.gravity_time = self.current_time
        self.movement_time = self.current_time
        self.rotation_time = self.current_time

        while self.running:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            if self.game.current_tetromino:
                self.current_time = pygame.time.get_ticks()
                self.pressed_keys = pygame.key.get_pressed()
            
                self.gravity()
                self.horizontal_movement()
                self.rotations()
                self.gogh.draw(self.game.active, self.game.landed)

        pygame.quit()
