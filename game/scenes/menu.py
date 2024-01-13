import pygame
import webbrowser

from game.scenes.base import SceneBase
from game.gui.button import Button


class SceneMenu(SceneBase):
    def __init__(self, screen):
        super().__init__(screen)
        self.buttons = [
            Button(200, 50, "Play", self.switch_to_setter, "game"),
            # Button(200, 50, "Leaderboard", self.switch_to_setter, "leaderboard"),
            Button(200, 50, "Settings", self.switch_to_setter, "settings"),
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
