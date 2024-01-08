import pygame
import random
import typing
import json

from game.van_gogh import VanGogh
from game.game import Game


class Engine:
    def __init__(self) -> None:
        self.config = self.read_cfg()
        pygame.init()
        self.clock = pygame.time.Clock()
        self.game_screen = pygame.display.set_mode(
            (self.config["resolution"]["width"], self.config["resolution"]["height"]),
            pygame.RESIZABLE,
        )
        pygame.display.set_caption(self.config["window_caption"])
        self.gogh = VanGogh(self.game_screen)
        self.game = Game()
        self.fps = self.config["fps"]
        self.gravity_time = None
        self.gravity_time_timeout_default = self.config["gravity_timeout"]["standard"]
        self.gravity_time_timeout_fast = self.config["gravity_timeout"]["fast"]
        self.gravity_time_timeout = self.gravity_time_timeout_default
        self.movement_time = None
        self.movement_time_timeout = self.config["movement_timeout"]
        self.rotation_time = None
        self.rotation_time_timeout = self.config["rotation_timeout"]
        self.pause_time = None
        self.pause_time_timeout = self.config["pause_timeout"]
        self.running = False
        self.paused = False
        self.current_time = None
        self.pressed_keys = None
        self.tetromino_types = ["j", "l", "s", "t", "z", "o", "i"]
        self.tetromino_counter = len(self.tetromino_types)
        self.spawn_point = (self.config["spawn"]["x"], self.config["spawn"]["y"])
        self.new_state = True

    def read_cfg(self) -> typing.Dict:
        with open("./cfg/game.json") as f:
            config = json.load(f)
        return config

    def tetrominos_bag(self) -> str:
        if self.tetromino_counter == len(self.tetromino_types):
            self.tetromino_counter = 0
            random.shuffle(self.tetromino_types)
        tetromino_type = self.tetromino_types[self.tetromino_counter]
        self.tetromino_counter += 1
        return tetromino_type

    def gravity(self) -> None:
        if self.pressed_keys[pygame.K_DOWN]:
            self.gravity_time_timeout = self.gravity_time_timeout_fast
        else:
            self.gravity_time_timeout = self.gravity_time_timeout_default
        elapsed_time = self.current_time - self.gravity_time
        if elapsed_time >= self.gravity_time_timeout:
            self.new_state = True
            self.gravity_time = self.current_time
            if not self.game.move_tetromino_down():
                self.game.push_to_landed()
                if not self.game.spawn_tetromino(
                    self.tetrominos_bag(), self.spawn_point[0], self.spawn_point[1]
                ):
                    self.running = False
                    print("Game over!")

    def horizontal_movement(self) -> None:
        if self.pressed_keys[pygame.K_RIGHT] or self.pressed_keys[pygame.K_LEFT]:
            elapsed_time = self.current_time - self.movement_time
            if elapsed_time >= self.movement_time_timeout:
                self.new_state = True
                if self.pressed_keys[pygame.K_LEFT]:
                    if self.game.move_tetromino_left():
                        self.movement_time = self.current_time
                elif self.pressed_keys[pygame.K_RIGHT]:
                    if self.game.move_tetromino_right():
                        self.movement_time = self.current_time

    def rotations(self) -> None:
        if self.pressed_keys[pygame.K_UP]:
            elapsed_time = self.current_time - self.rotation_time
            if elapsed_time >= self.rotation_time_timeout:
                self.new_state = True
                if self.game.rotate_tetromino():
                    self.rotation_time = self.current_time

    def pause(self) -> None:
        if self.pressed_keys[pygame.K_ESCAPE]:
            elapsed_time = self.current_time - self.pause_time
            if elapsed_time >= self.pause_time_timeout:
                self.paused = not self.paused
                if self.paused:
                    print("Game paused")
                else:
                    print("Game unpaused")
                self.pause_time = self.current_time

    def prepare(self) -> None:
        self.game.spawn_tetromino(
            self.tetrominos_bag(), self.spawn_point[0], self.spawn_point[1]
        )
        self.current_time = pygame.time.get_ticks()
        self.gravity_time = self.current_time
        self.movement_time = self.current_time
        self.rotation_time = self.current_time
        self.pause_time = self.current_time
        self.running = True

    def start(self) -> None:
        self.prepare()
        while self.running:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.current_time = pygame.time.get_ticks()
            self.pressed_keys = pygame.key.get_pressed()
            self.pause()
            if not self.paused:
                if self.game.current_tetromino:
                    self.horizontal_movement()
                    self.rotations()
                    self.gravity()
                if self.new_state:
                    self.gogh.draw(self.game.active, self.game.landed)
                    self.new_state = False

        pygame.quit()
