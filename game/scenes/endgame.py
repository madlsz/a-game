from game.scenes.base import SceneBase


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
