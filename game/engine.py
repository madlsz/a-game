import pygame
import numpy as np

from game.scenes.scenes import SceneMenu


def run():
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
        active_scene = active_scene.next
        clock.tick(60)

    pygame.quit()
