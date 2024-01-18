import pygame

from game.scenes.base import SceneBase
from game.gui.button import Button


class SceneEndgame(SceneBase):
    def __init__(self, screen):
        super().__init__(screen)
        self.button_background_color = (64, 64, 64, 150)
        self.endgame_screen = pygame.Surface(
            (self.screen.get_width() / 14 * 10, self.screen.get_height() * 0.4),
            pygame.SRCALPHA,
        )
        self.buttons = [
            Button(
                self.button_width,
                self.button_height,
                "Play again",
                self.switch_to_setter,
                "game",
                background_color=self.button_background_color,
            ),
            Button(
                self.button_width,
                self.button_height,
                "Menu",
                self.switch_to_setter,
                "menu",
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
                    if button.click():
                        self.new_state = True

    def update(self):
        pass

    def render(self):
        if self.new_state:
            self.new_state = False
            self.endgame_screen.fill((0, 99, 99, 0))
            text = self.font_large.render("GAME OVER", True, (255, 255, 255))
            self.endgame_screen.blit(
                text, ((self.endgame_screen.get_width() - text.get_width()) // 2, 0)
            )
            for i, button in enumerate(self.buttons):
                button.x = (self.endgame_screen.get_width() - button.width) // 2
                button.y = (
                    button.height * (i + 1) * 1.3
                    + (self.screen.get_height() - self.endgame_screen.get_height()) // 2
                )
                self.endgame_screen.blit(
                    button.surface,
                    (
                        button.x,
                        button.y
                        - (self.screen.get_height() - self.endgame_screen.get_height())
                        // 2,
                    ),
                )
            self.screen.blit(
                self.endgame_screen,
                (
                    0,
                    (self.screen.get_height() - self.endgame_screen.get_height()) // 2,
                ),
            )
            pygame.display.update()
