import pygame
import numpy as np
from collections import defaultdict


class VanGogh():
    def __init__(self, screen, border_thickness = 1, border_color = (0, 0, 0), background_color = (66, 66, 66)):
        self.screen = screen
        self.border_thickness = border_thickness
        self.border_color = border_color
        self.background_color = background_color

        self.color_map = defaultdict(lambda : (255, 255, 255))
        self.color_map[73] = (55, 255, 255)
        self.color_map[74] = (51, 51, 255)
        self.color_map[76] = (255, 128, 0)
        self.color_map[79] = (255, 255, 51)
        self.color_map[83] = (0, 255, 0)
        self.color_map[84] = (255, 0, 255)
        self.color_map[90] = (255, 51, 51)

    @property
    def width(self):
        return self.screen.get_width()
    
    @property
    def height(self):
        return self.screen.get_height()
    
    @property
    def tile_width(self):
        return self.width // 10

    @property
    def tile_height(self):
        return self.height // 20
    

    def draw(self, active, landed):
        self.screen.fill(self.background_color)
        board = active + landed
        for (y, x), value in np.ndenumerate(board):
            if value != 0:
                pygame.draw.rect(self.screen, self.border_color, pygame.Rect(x * self.tile_width, y * self.tile_height, self.tile_width, self.tile_height))
                pygame.draw.rect(self.screen, self.color_map[value], pygame.Rect(x * self.tile_width - self.border_thickness, y * self.tile_height - self.border_thickness, self.tile_width - self.border_thickness, self.tile_height - self.border_thickness))
        pygame.display.update()

        