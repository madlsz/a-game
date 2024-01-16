from abc import ABC, abstractmethod
import pygame


class SceneBase(ABC):
    def __init__(self, screen: pygame.Surface) -> None:
        self.next = self
        self.screen = screen
        self.new_state = True
        self.switch_to = None
        self.button_background_color = (64, 64, 64, 255)
        self.button_width = self.screen.get_width() // 2.8
        self.button_height = self.button_width * 0.2

    def switch_to_setter(self, id: str) -> None:
        self.switch_to = id

    @abstractmethod
    def process_input(self, events, keys_pressed):
        """
        This method is meant to receive all the events that happened since the last frame.
        """
        pass

    @abstractmethod
    def update(self):
        """
        This method is meant to contain the logic of a scene
        """
        pass

    @abstractmethod
    def render(self):
        """
        This method is meant to be responsible for rendering each scene to self.screen object
        """
        pass

    def switch_to_scene(self, next_scene):
        """
        This method switches the self.next attribute to the given scene
        """
        self.next = next_scene

    def terminate(self):
        """
        Sets self.next to None
        """
        self.switch_to_scene(None)
