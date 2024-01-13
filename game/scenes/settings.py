import collections
import json
import typing
import pygame

from game.gui.button import Button
from game.gui.toggle import Toggle
from game.scenes.base import SceneBase


# what to put in settings?
# random tetrominos
# next piece preview
# language?


class SceneSettings(SceneBase):
    def __init__(self, screen):
        super().__init__(screen)
        self.buttons = [
            Button(
                200,
                50,
                "return",
                self.switch_to_setter,
                "menu",
                id="return",
            ),
            Button(
                200,
                50,
                "save changes",
                self.save_changes,
                id="save",
            ),
            Button(
                200,
                50,
                "Settings",
                None,
                background_color=(0, 0, 0, 0),
                id="settings",
            ),
            Button(
                350,
                50,
                "",
                self.random_pieces_toggle,
                id="random_pieces_toggle",
            ),
        ]

        self.engine_cfg = None
        self.gogh_cfg = None
        self.read_cfg()

    def random_pieces_toggle(self):
        self.engine_cfg["random_pieces"] = not self.engine_cfg["random_pieces"]

    def save_changes(self):
        with open("./cfg/engine.json", "w") as f:
            json.dump(self.engine_cfg, f, indent=4)
        with open("./cfg/gogh.json", "w") as f:
            json.dump(self.gogh_cfg, f, indent=4)

    def read_cfg(self) -> None:
        with open("./cfg/engine.json") as f:
            self.engine_cfg = json.load(f)
        with open("./cfg/gogh.json") as f:
            self.gogh_cfg = json.load(f)

    def process_input(self, events, keys_pressed):
        for event in events:
            if event.type == pygame.QUIT:
                self.terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.click():
                        self.new_state = True

    def update(self):
        pass

    def render(self):
        if self.new_state:
            self.new_state = False
            self.screen.fill((0, 99, 99))
            i = -1
            for button in self.buttons:
                i += 1
                if button.id == "return":
                    button.x = button.width * 0.05
                    button.y = self.screen.get_height() - button.height * 1.2
                    self.screen.blit(button.surface, (button.x, button.y))
                elif button.id == "save":
                    button.x = self.screen.get_width() - button.width * 1.05
                    button.y = self.screen.get_height() - button.height * 1.2
                    self.screen.blit(button.surface, (button.x, button.y))
                elif button.id == "settings":
                    button.x = (self.screen.get_width() - button.width) // 2
                    button.y = 10 * (i + 1)
                    self.screen.blit(button.surface, (button.x, button.y))
                elif button.id == "random_pieces_toggle":
                    if self.engine_cfg["random_pieces"]:
                        button.edit_caption("Random pieces: True")
                    else:
                        button.edit_caption("Random pieces: False")
                    button.x = (self.screen.get_width() - button.width) // 2
                    button.y = 50 * (i + 1)
                    self.screen.blit(button.surface, (button.x, button.y))
            pygame.display.update()
