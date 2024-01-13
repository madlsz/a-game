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
            )
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
                if button.id == "return":
                    button.x = button.width * 0.05
                    button.y = self.screen.get_height() - button.height * 1.2
                    self.screen.blit(button.surface, (button.x, button.y))
                else:
                    button.x = (self.screen.get_width() - button.width) // 2
                    button.y = 100 * (i + 1)
                    self.screen.blit(button.surface, (button.x, button.y))
            pygame.display.update()
