import typing
import json
import random
import webbrowser
import collections
import pygame
import numpy as np

from game.scenes.base import SceneBase
from game.gui.button import Button
from game.logic import Game
from game.gui.van_gogh import VanGogh
from game import tetrominos


class SceneMenu(SceneBase):
    def __init__(self, screen):
        super().__init__(screen)
        self.buttons = [
            Button(
                200, 50, "Play", lambda: self.switch_to_scene(SceneGame(self.screen))
            ),
            Button(
                200,
                50,
                "Leaderboard",
                lambda: self.switch_to_scene(SceneLeaderboard(self.screen)),
            ),
            Button(
                200,
                50,
                "Github page",
                webbrowser.open,
                "https://github.com/madlsz/a-game",
            ),
            Button(200, 50, "Quit", self.terminate),
        ]

    def process_input(self, events, keys_pressed):
        for event in events:
            if event.type == pygame.QUIT:
                self.terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    button.click()

    def update(self):
        pass

    def render(self):
        if self.new_state:
            self.new_state = False
            self.screen.fill((0, 99, 99))
            for i, button in enumerate(self.buttons):
                button.x = (self.screen.get_width() - button.width) // 2
                button.y = 100 * (i + 2)
                self.screen.blit(button.surface, (button.x, button.y))
            pygame.display.update()


class SceneEndgame(SceneBase):
    def __init__(self, screen, score):
        super().__init__(screen)
        self.score = score
        self.buttons = []

    def process_input(self, events, keys_pressed):
        return super().process_input(events, keys_pressed)

    def update(self):
        return super().update()

    def render(self, screen):
        return super().render(screen)


class SceneLeaderboard(SceneBase):
    def __init__(self, screen):
        super().__init__(screen)
        self.buttons = [
            Button(
                200,
                50,
                "return",
                lambda: self.switch_to_scene(SceneMenu(self.screen)),
                id="return",
            )
        ]
        self.leaderboard = self.read_leaderboard()
        self.leaderboard = collections.OrderedDict(
            sorted(self.leaderboard.items(), key=lambda x: x[1], reverse=True)
        )
        self.buttons.append(
            Button(
                200,
                50,
                "Top scores:",
                None,
                background_color=(0, 0, 0, 0),
            )
        )
        for i, key in enumerate(self.leaderboard):
            self.buttons.append(
                Button(
                    200,
                    50,
                    f"{i+1}.{key} {self.leaderboard[key]}",
                    None,
                    background_color=(0, 0, 0, 0),
                )
            )

    def read_leaderboard(self) -> typing.Dict:
        with open("leaderboard.json") as f:
            leaderboard = json.load(f)
        return leaderboard

    def process_input(self, events, keys_pressed):
        for event in events:
            if event.type == pygame.QUIT:
                self.terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    button.click()

    def update(self):
        pass

    def render(self):
        if self.new_state:
            self.new_state = False
            self.screen.fill((0, 99, 99))
            for i, button in enumerate(self.buttons):
                if button.id == "return":
                    button.x = button.width * 0.05
                    button.y = self.screen.get_height() - button.height * 1.2
                    self.screen.blit(button.surface, (button.x, button.y))
                else:
                    button.x = (self.screen.get_width() - button.width) // 2
                    button.y = 100 * (i + 1)
                    self.screen.blit(button.surface, (button.x, button.y))
            pygame.display.update()


class SceneGame(SceneBase):
    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__(screen)
        self.config = self.read_cfg()
        self.prepare_tetrominos()
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
        self.new_preview = True
        self.new_level = True
        self.new_score = True
        self.new_buttons = True
        self.new_lines = True
        self.are = 100
        self.game.spawn_tetromino(
            self.draw_tetromino(),
            self.config["spawn"]["x"],
            self.config["spawn"]["y"],
        )
        self.buttons = [
            Button(
                150,
                50,
                "Menu",
                lambda: self.switch_to_scene(SceneMenu(self.screen)),
                background_color=(50, 50, 50, 255),
            ),
            Button(
                150, 50, "Pause", self.toggle_pause, background_color=(50, 50, 50, 255)
            ),
        ]

        # used to calculate vertical speed (ms/row)
        self.tick_const = 1000 / 60.0988

    def read_cfg(self) -> typing.Dict:
        with open("./cfg/engine.json") as f:
            config = json.load(f)
        return config

    @property
    def gravity_time_timeout_standard(self) -> int:
        return np.rint(
            self.config["ticks_per_row"][str(self.game.level)] * self.tick_const
        )

    @property
    def gravity_time_timeout_fast(self) -> int:
        return np.rint(self.config["ticks_per_row"]["29"] * self.tick_const)

    def prepare_tetrominos(self) -> None:
        """
        Prepares the next "bag" of tetrominos,
        Depends on the "random_pieces" flag in config file
        Random pieces enabled means that the next piece is entirely random
        Random pieces disabled means that pieces come in a shuffled collection
        """
        if not self.config["random_pieces"]:
            self.tetromino_types = self.config["tetromino_types"]
            random.shuffle(self.tetromino_types)
        else:
            self.tetromino_types = [
                random.choice(self.config["tetromino_types"])
                for _ in range(len(self.config["tetromino_types"]))
            ]

    def draw_tetromino(self) -> str:
        tetromino_type = self.tetromino_types[self.tetromino_counter]
        self.tetromino_counter += 1
        if self.tetromino_counter == len(self.tetromino_types):
            self.tetromino_counter = 0
            self.prepare_tetrominos()
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
                self.new_lines = True
                pygame.time.wait(self.are)
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
                if self.keys_pressed[pygame.K_LEFT]:
                    if self.game.move_tetromino_left():
                        self.new_state = True
                        self.movement_time = self.current_time
                elif self.keys_pressed[pygame.K_RIGHT]:
                    if self.game.move_tetromino_right():
                        self.new_state = True
                        self.movement_time = self.current_time

    def rotations(self) -> None:
        if self.keys_pressed[pygame.K_z] or self.keys_pressed[pygame.K_x]:
            elapsed_time = self.current_time - self.rotation_time
            if elapsed_time >= self.config["rotation_timeout"]:
                if self.keys_pressed[pygame.K_z]:
                    clockwise = False
                elif self.keys_pressed[pygame.K_x]:
                    clockwise = True
                if self.game.rotate_tetromino(clockwise):
                    self.new_state = True
                    self.rotation_time = self.current_time

    def pause(self) -> bool:
        if self.keys_pressed[pygame.K_p]:
            elapsed_time = self.current_time - self.pause_time
            if elapsed_time >= self.config["pause_timeout"]:
                self.toggle_pause()
                self.pause_time = self.current_time
        return self.paused

    def toggle_pause(self) -> None:
        self.paused = not self.paused
        if self.paused:
            self.gogh.draw_pause()
        else:
            self.gogh.draw_game(self.game.active, self.game.landed)

    def process_input(
        self,
        events: typing.List[pygame.event.Event],
        keys_pressed: pygame.key.ScancodeWrapper,
    ) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                self.terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    button.click()
        self.keys_pressed = keys_pressed

    def update(self) -> None:
        self.current_time = pygame.time.get_ticks()
        if not self.pause():
            if self.game.current_tetromino:
                self.horizontal_movement()
                self.rotations()
                self.gravity()

    def render(self) -> None:
        if self.new_state:
            self.new_state = False
            self.gogh.draw_game(self.game.active, self.game.landed)
        if self.new_preview:
            self.new_preview = False
            self.gogh.draw_preview(
                tetrominos.create_instance(self.tetromino_types[self.tetromino_counter])
            )
        if self.new_level:
            self.new_level = False
            self.gogh.draw_level(self.game.level)
        if self.new_score:
            self.new_score = False
            self.gogh.draw_score(self.game.score)
        if self.new_buttons:
            self.new_buttons = False
            self.gogh.draw_buttons(self.buttons)
        if self.new_lines:
            self.new_lines = False
            self.gogh.draw_lines(self.game.cleared_lines)
