import pygame
import typing
import json
import random
import webbrowser
import collections

from game.button import Button
from game.logic import Game
from game.van_gogh import VanGogh
from game import tetrominos
from game.scenes import SceneBase


class SceneMenu(SceneBase):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.buttons = [
            Button(200, 50, "Play", self.switch_to_game),
            Button(200, 50, "Leaderboard", self.swithc_to_leaderboard),
            Button(
                200,
                50,
                "Github page",
                webbrowser.open,
                "https://github.com/madlsz/a-game",
            ),
            Button(200, 50, "Quit", self.terminate),
        ]
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

    def swithc_to_leaderboard(self):
        self.switch_to_scene(SceneLeaderboard(self.screen))
        self.new_state = False

    def render(self):
        if self.new_state:
            self.new_state = False
            self.screen.fill((0, 99, 99))
            for i, button in enumerate(self.buttons):
                button.x = (self.screen.get_width() - button.width) // 2
                button.y = 100 * (i + 2)
                self.screen.blit(button.surface, (button.x, button.y))
            pygame.display.update()


class SceneLeaderboard(SceneBase):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.buttons = [Button(200, 50, "return", self.switch_to_menu, id="return")]
        self.new_state = True
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

    def switch_to_menu(self):
        self.switch_to_scene(SceneMenu(self.screen))
        self.new_state = False

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
                    # button.y = 100 * (i + 2)
                    self.screen.blit(button.surface, (button.x, button.y))
                else:
                    button.x = (self.screen.get_width() - button.width) // 2
                    button.y = 100 * (i + 1)
                    self.screen.blit(button.surface, (button.x, button.y))
            pygame.display.update()


class SceneGame(SceneBase):
    def __init__(self, screen: pygame.Surface):
        super().__init__()
        self.config = self.read_cfg()
        random.shuffle(self.config["tetromino_types"])
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
        self.new_buttons = True
        self.game.spawn_tetromino(
            self.draw_tetromino(),
            self.config["spawn"]["x"],
            self.config["spawn"]["y"],
        )
        self.landed = False
        self.landed_timeout = 800
        self.buttons = [
            Button(
                150, 50, "Menu", self.switch_to_menu, background_color=(50, 50, 50, 255)
            ),
            Button(
                150, 50, "Pause", self.toggle_pause, background_color=(50, 50, 50, 255)
            ),
        ]

    def read_cfg(self) -> typing.Dict:
        with open("./cfg/engine.json") as f:
            config = json.load(f)
        return config

    def switch_to_menu(self):
        self.switch_to_scene(SceneMenu(self.screen))

    @property
    def gravity_time_timeout_standard(self) -> int:
        if not self.landed:
            return round(
                self.config["ticks_per_row"][str(self.game.level)]
                * 1000
                / self.config["tps"]
            )
        else:
            return self.landed_timeout

    @property
    def gravity_time_timeout_fast(self) -> int:
        return round(self.config["ticks_per_row"]["29"] * 1000 / self.config["tps"])
        if not self.landed:
            return round(self.config["ticks_per_row"]["29"] * 1000 / self.config["tps"])
        else:
            return self.landed_timeout

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
                if not self.landed:
                    self.new_state = False
                    self.landed = True
                else:
                    self.landed = False
                    self.game.push_to_landed()
                    self.new_preview = True
                    self.new_level = True
                    self.new_score = True
                    pygame.time.wait(500)
                    if not self.game.spawn_tetromino(
                        self.draw_tetromino(),
                        self.config["spawn"]["x"],
                        self.config["spawn"]["y"],
                    ):
                        self.new_state = False
                        self.switch_to_scene(SceneMenu(self.screen))
                    else:
                        self.new_state = True
            else:
                self.landed = False

    def horizontal_movement(self) -> None:
        if self.keys_pressed[pygame.K_RIGHT] or self.keys_pressed[pygame.K_LEFT]:
            elapsed_time = self.current_time - self.movement_time
            if elapsed_time >= self.config["movement_timeout"]:
                # self.new_state = True
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
        if self.keys_pressed[pygame.K_p]:
            elapsed_time = self.current_time - self.pause_time
            if elapsed_time >= self.config["pause_timeout"]:
                self.toggle_pause()
                self.pause_time = self.current_time
        return self.paused

    def toggle_pause(self):
        self.paused = not self.paused
        if self.paused:
            self.gogh.draw_pause()
        else:
            self.gogh.draw_game(self.game.active, self.game.landed)

    def process_input(self, events, keys_pressed):
        for event in events:
            if event.type == pygame.QUIT:
                self.terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    button.click()
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
        if self.new_buttons:
            self.new_buttons = False
            self.gogh.draw_buttons(self.buttons)


def run():
    pygame.init()
    height = int(pygame.display.Info().current_h * 0.8) // 20 * 20
    width = int(7 * height // 10)
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    pygame.display.set_caption("a Game")
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
