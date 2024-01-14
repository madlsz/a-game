import pygame

from game.scenes.base import SceneBase
from game.gui.button import Button


class SceneEndgame(SceneBase):
    def __init__(self, screen, score, level, lines):
        super().__init__(screen)
        self.score = score
        self.level = level
        self.lines = lines
        self.endgame_screen = pygame.Surface(
            (self.screen.get_width(), self.screen.get_height() * 0.4)
        )
        self.buttons = [
            Button(
                200,
                50,
                "Play again",
                self.switch_to_setter,
                "game",
                background_color=(0, 0, 0, 255),
            ),
            Button(
                200,
                50,
                "Menu",
                self.switch_to_setter,
                "menu",
                background_color=(0, 0, 0, 255),
            ),
            Button(
                200,
                50,
                "Quit",
                self.terminate,
                background_color=(0, 0, 0, 255),
            ),
        ]

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
            # self.screen.fill((0, 99, 99))
            self.endgame_screen.fill((0, 99, 99))
            for i, button in enumerate(self.buttons):
                button.x = (self.endgame_screen.get_width() - button.width) // 2
                button.y = button.height * (i + 1)
                self.endgame_screen.blit(button.surface, (button.x, button.y))
            self.screen.blit(self.endgame_screen, (0, 0))
            pygame.display.update()
