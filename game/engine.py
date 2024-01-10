from abc import ABC, abstractmethod
import pygame
import typing
import json
import random

from game.button import Button
from game.logic import Game
from game.van_gogh import VanGogh
from game import tetrominos


class SceneBase(ABC):
    def __init__(self):
        self.next = self

    @abstractmethod
    # This method will receive all the events that happened since the last frame.
    def process_input(self, events, keys_pressed):
        pass

    @abstractmethod
    # Put your game logic in here for the scene
    def update(self):
        pass

    @abstractmethod
    # Put your render code here. It will receive the main screen Surface as input.
    def render(self, screen):
        pass

    def switch_to_scene(self, next_scene):
        self.next = next_scene

    def terminate(self):
        self.switch_to_scene(None)


class SceneMenu(SceneBase):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.buttons = []
        self.buttons.append(Button(100, 50, "play", self.switch_to_game))
        self.buttons.append(Button(100, 50, "quit", self.terminate))
        self.new_state = True

    def process_input(self, events, keys_pressed):
        for event in events:
            if event.type == pygame.QUIT:
                self.terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    button.click()

    def update(self):
        pass

    def switch_to_game(self):
        self.switch_to_scene(SceneGame(self.screen))
        self.new_state = False

    def render(self):
        if self.new_state:
            self.new_state = False
            self.screen.fill((0, 0, 255))
            for i, button in enumerate(self.buttons):
                button.x = (self.screen.get_width() - button.width) // 2
                button.y = 100 * (i + 2)
                self.screen.blit(button.surface, (button.x, button.y))
            pygame.display.update()


class SceneGame(SceneBase):
    def __init__(self, screen: pygame.Surface):
        super().__init__()
        self.config = self.read_cfg()
        self.screen = screen
        self.game = Game()
        self.gogh = VanGogh(screen)
        self.current_time = pygame.time.get_ticks()
        self.gravity_time = self.current_time
        self.movement_time = self.current_time
        self.rotation_time = self.current_time
        self.pause_time = self.current_time
        self.tetromino_counter = 0
        self.keys_pressed = None
        self.paused = False
        self.new_state = True
        self.new_preview = True
        self.new_level = True
        self.new_score = True
        self.game.spawn_tetromino(self.draw_tetromino())

    def read_cfg(self) -> typing.Dict:
        with open("./cfg/engine.json") as f:
            config = json.load(f)
        return config

    @property
    def gravity_time_timeout_standard(self) -> int:
        return round(
            self.config["ticks_per_row"][str(self.game.level)]
            * 1000
            / self.config["tps"]
        )

    @property
    def gravity_time_timeout_fast(self) -> int:
        return round(self.config["ticks_per_row"]["29"] * 1000 / self.config["tps"])

    def draw_tetromino(self) -> str:
        tetromino_type = self.config["tetromino_types"][self.tetromino_counter]
        self.tetromino_counter += 1
        if self.tetromino_counter == len(self.config["tetromino_types"]):
            self.tetromino_counter = 0
            random.shuffle(self.config["tetromino_types"])
        return tetromino_type

    def gravity(self) -> None:
        elapsed_time = self.current_time - self.gravity_time
        if elapsed_time >= (
            self.gravity_time_timeout_fast
            if self.keys_pressed[pygame.K_DOWN]
            else self.gravity_time_timeout_standard
        ):
            self.new_state = True
            self.gravity_time = self.current_time
            if not self.game.move_tetromino_down():
                self.game.push_to_landed()
                self.new_preview = True
                self.new_level = True
                self.new_score = True
                if not self.game.spawn_tetromino(
                    self.draw_tetromino(),
                    self.config["spawn"]["x"],
                    self.config["spawn"]["y"],
                ):
                    self.new_state = False
                    self.switch_to_scene(SceneMenu(self.screen))

    def horizontal_movement(self) -> None:
        if self.keys_pressed[pygame.K_RIGHT] or self.keys_pressed[pygame.K_LEFT]:
            elapsed_time = self.current_time - self.movement_time
            if elapsed_time >= self.config["movement_timeout"]:
                self.new_state = True
                if self.keys_pressed[pygame.K_LEFT]:
                    if self.game.move_tetromino_left():
                        self.new_state = True
                        self.movement_time = self.current_time
                elif self.keys_pressed[pygame.K_RIGHT]:
                    if self.game.move_tetromino_right():
                        self.new_state = True
                        self.movement_time = self.current_time

    def rotations(self) -> None:
        if self.keys_pressed[pygame.K_UP]:
            elapsed_time = self.current_time - self.rotation_time
            if elapsed_time >= self.config["rotation_timeout"]:
                if self.game.rotate_tetromino():
                    self.new_state = True
                    self.rotation_time = self.current_time

    def pause(self) -> bool:
        if self.keys_pressed[pygame.K_ESCAPE]:
            elapsed_time = self.current_time - self.pause_time
            if elapsed_time >= self.config["pause_timeout"]:
                self.paused = not self.paused
                self.pause_time = self.current_time
        return self.paused

    def process_input(self, events, keys_pressed):
        for event in events:
            if event.type == pygame.QUIT:
                self.terminate()
        self.keys_pressed = keys_pressed

    def update(self):
        self.current_time = pygame.time.get_ticks()
        if not self.pause():
            if self.game.current_tetromino:
                self.horizontal_movement()
                self.rotations()
                self.gravity()

    def render(self):
        if self.new_state:
            self.new_state = False
            self.gogh.draw_game(self.game.active, self.game.landed)
        if self.new_preview:
            self.new_preview = False
            self.gogh.draw_preview(
                tetrominos.create_instance(
                    self.config["tetromino_types"][self.tetromino_counter]
                )
            )
        if self.new_level:
            self.new_level = False
            self.gogh.draw_level(self.game.level)
        if self.new_score:
            self.new_score = False
            self.gogh.draw_score(self.game.score)


def run():
    pygame.init()
    height = int(pygame.display.Info().current_h * 0.8) // 20 * 20
    width = int(7 * height // 10)
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    active_scene = SceneMenu(screen)

    while active_scene != None:
        events = pygame.event.get()
        keys_pressed = pygame.key.get_pressed()
        active_scene.process_input(events, keys_pressed)
        active_scene.update()
        active_scene.render()
        active_scene = active_scene.next
        clock.tick(60)

    pygame.quit()
