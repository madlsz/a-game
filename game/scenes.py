from abc import ABC, abstractmethod
import pygame


class SceneBase(ABC):
    def __init__(self, screen: pygame.Surface) -> None:
        self.next = self
        self.screen = screen
        self.new_state = True

    @abstractmethod
    # This method will receive all the events that happened since the last frame.
    def process_input(self, events, keys_pressed):
        pass

    @abstractmethod
    # Put your game logic in here for the scene
    def update(self):
        pass

    @abstractmethod
    # Put your render code here. It will receive the main screen Surface as input.
    def render(self):
        pass

    def switch_to_scene(self, next_scene):
        self.next = next_scene

    def terminate(self):
        self.switch_to_scene(None)
