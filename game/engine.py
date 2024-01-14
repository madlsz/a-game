import pygame
import numpy as np

from game.scenes.endgame import SceneEndgame
from game.scenes.game import SceneGame
from game.scenes.leaderboard import SceneLeaderboard
from game.scenes.menu import SceneMenu
from game.scenes.settings import SceneSettings


class Engine:
    def __init__(self):
        pygame.init()
        self.height = np.rint(pygame.display.Info().current_h * 0.8) // 20 * 20
        self.width = np.rint(7 * self.height // 10)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("a Game")
        self.active_scene = SceneMenu(self.screen)
        self.switch_to_scene = {
            "menu": lambda scene: scene.switch_to_scene(SceneMenu(self.screen)),
            "endgame": lambda scene: scene.switch_to_scene(SceneEndgame(self.screen)),
            "game": lambda scene: scene.switch_to_scene(SceneGame(self.screen)),
            "settings": lambda scene: scene.switch_to_scene(SceneSettings(self.screen)),
            "endgame": lambda scene: scene.switch_to_scene(
                SceneEndgame(
                    self.screen,
                )
            ),
        }

    def run(self):
        while self.active_scene is not None:
            events = pygame.event.get()
            keys_pressed = pygame.key.get_pressed()
            self.active_scene.process_input(events, keys_pressed)
            self.active_scene.update()
            self.active_scene.render()

            if self.active_scene.switch_to is not None:
                self.switch_to_scene[self.active_scene.switch_to](self.active_scene)

            self.active_scene = self.active_scene.next
            self.clock.tick(60)

        pygame.quit()
