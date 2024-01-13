import pygame
import numpy as np

from game.scenes.endgame import SceneEndgame
from game.scenes.game import SceneGame
from game.scenes.leaderboard import SceneLeaderboard
from game.scenes.menu import SceneMenu


def run():
    switch_to_menu = lambda scene: scene.switch_to_scene(SceneMenu(scene.screen))
    switch_to_endgame = lambda scene: scene.switch_to_scene(SceneEndgame(scene.screen))
    switch_to_game = lambda scene: scene.switch_to_scene(SceneGame(scene.screen))
    switch_to_lb = lambda scene: scene.switch_to_scene(SceneLeaderboard(scene.screen))

    pygame.init()
    height = np.rint(pygame.display.Info().current_h * 0.8) // 20 * 20
    width = np.rint(7 * height // 10)
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

        if active_scene.switch_to == "menu":
            switch_to_menu(active_scene)
        elif active_scene.switch_to == "endgame":
            switch_to_endgame(active_scene)
        elif active_scene.switch_to == "game":
            switch_to_game(active_scene)
        elif active_scene.switch_to == "leaderboard":
            switch_to_lb(active_scene)

        active_scene = active_scene.next
        clock.tick(60)

    pygame.quit()
