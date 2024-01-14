import pygame

from game.scenes.base import SceneBase
from game.gui.button import Button


class SceneEndgame(SceneBase):
    def __init__(self, screen):
        super().__init__(screen)
        self.endgame_screen = pygame.Surface(
            (self.screen.get_width() / 14 * 10, self.screen.get_height() * 0.4),
            pygame.SRCALPHA,
        )
        self.buttons = [
            Button(
                200,
                50,
                "Play again",
                self.switch_to_setter,
                "game",
                background_color=(0, 0, 0, 0),
            ),
            Button(
                200,
                50,
                "Menu",
                self.switch_to_setter,
                "menu",
                background_color=(0, 0, 0, 0),
            ),
            Button(
                200,
                50,
                "Quit",
                self.terminate,
                background_color=(0, 0, 0, 0),
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
            self.endgame_screen.fill((0, 99, 99, 0))
            for i, button in enumerate(self.buttons):
                button.x = (self.endgame_screen.get_width() - button.width) // 2
                button.y = button.height * (i + 1)
                self.endgame_screen.blit(button.surface, (button.x, button.y))
            self.screen.blit(self.endgame_screen, (0, 0))
            pygame.display.update()
