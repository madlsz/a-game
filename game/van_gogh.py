import pygame
import numpy as np
from collections import defaultdict
import json


class VanGogh:
    def __init__(
        self,
        main_screen: pygame.Surface,
        game_screen: pygame.Surface,
        preview_screen: pygame.Surface
    ) -> None:
        self.main_screen = main_screen
        self.game_screen = game_screen
        self.preview_screen = preview_screen
        self.border_color = None
        self.background_color = None
        self.color_map = None
        self.read_cfg()

    def read_cfg(self) -> None:
        with open("./cfg/gogh.json") as f:
            config = json.load(f)
        self.color_map = defaultdict(lambda: config["default_tile_color"])
        for tile in config["tiles_colors"]:
            self.color_map[int(tile)] = config["tiles_colors"][tile]
        self.border_color = config["border_color"]
        self.background_color = config["background_color"]

    @property
    def width(self) -> int:
        return self.game_screen.get_width()

    @property
    def height(self) -> int:
        return self.game_screen.get_height()

    @property
    def tile_width(self) -> int:
        return self.width // 10

    @property
    def tile_height(self) -> int:
        return self.height // 20

    def draw_game(self, active: np.ndarray, landed: np.ndarray) -> None:
        """
        Draws the game (board)
        """
        self.game_screen.fill(self.background_color)
        board = active + landed
        for (y, x), value in np.ndenumerate(board):
            if value != 0:
                pygame.draw.rect(
                    self.game_screen,
                    self.color_map[value],
                    pygame.Rect(
                        x * self.tile_width,
                        y * self.tile_height,
                        self.tile_width,
                        self.tile_height,
                    ),
                )
        for x in range(0, self.width, self.tile_width):
            pygame.draw.line(
                self.game_screen, self.border_color, (x, 0), (x, self.height)
            )
        for y in range(0, self.height, self.tile_height):
            pygame.draw.line(
                self.game_screen, self.border_color, (0, y), (self.width, y)
            )
        self.main_screen.blit(self.game_screen, (0,0))
        pygame.display.update()

    def draw_preview(self, mask):
        """
        Draws the preview of the next tetromino
        """
        self.preview_screen.fill(self.background_color)
        for (y, x), value in np.ndenumerate(mask):
            if value != 0:
                pygame.draw.rect(
                    self.preview_screen,
                    self.color_map[value],
                    pygame.Rect(
                        x * self.tile_width,
                        y * self.tile_height,
                        self.tile_width,
                        self.tile_height,
                    ),
                )
        self.main_screen.blit(self.preview_screen, (self.width, 0))
        pass
