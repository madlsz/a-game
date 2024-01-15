import pygame
import webbrowser

from game.scenes.base import SceneBase
from game.gui.button import Button


class SceneMenu(SceneBase):
    def __init__(self, screen):
        super().__init__(screen)
        self.buttons = [
            Button(
                self.button_width,
                self.button_height,
                "Menu",
                None,
                background_color=(0, 0, 0, 0),
            ),
            Button(
                self.button_width,
                self.button_height,
                "Play",
                self.switch_to_setter,
                "game",
                background_color=self.button_background_color,
            ),
            Button(
                self.button_width,
                self.button_height,
                "Settings",
                self.switch_to_setter,
                "settings",
                background_color=self.button_background_color,
            ),
            Button(
                self.button_width,
                self.button_height,
                "Github page",
                webbrowser.open,
                "https://github.com/madlsz/a-game",
                background_color=self.button_background_color,
            ),
            Button(
                self.button_width,
                self.button_height,
                "Quit",
                self.terminate,
                background_color=self.button_background_color,
            ),
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
            self.screen.fill((0, 0, 0))
            i = 1.5
            for button in self.buttons:
                button.x = (self.screen.get_width() - button.width) // 2
                button.y = button.height * (i + 1) * 1.8
                self.screen.blit(button.surface, (button.x, button.y))
                i += 1
            pygame.display.update()
