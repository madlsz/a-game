import pygame
import numpy as np
from collections import defaultdict
import json
import typing

from game import tetrominos


class VanGogh:
    def __init__(self, screen: pygame.Surface) -> None:
        self.main_screen = screen
        self.config = self.read_cfg()
        self.main_screen.fill(self.config["background_color"]["game"])
        pygame.display.update()
        self.color_map = defaultdict(lambda: self.config["default_tile_color"])
        for tile in self.config["tiles_colors"]:
            self.color_map[int(tile)] = self.config["tiles_colors"][tile]
        self.border_color = self.config["grid"]["color"]
        self.background_color = self.config["background_color"]["game"]

        self.game_screen = pygame.Surface(
            (screen.get_width() // 14 * 10, screen.get_height())
        )

        self.preview_screen = pygame.Surface(
            (self.tile_width * 4, self.tile_height * 4)
        )
        self.score_screen = pygame.Surface((self.tile_width * 4, self.tile_height * 3))
        self.level_screen = pygame.Surface((self.tile_width * 4, self.tile_height * 3))

        # pygame.display.set_caption(self.config["window_caption"])
        self.font_large = pygame.font.Font(
            self.config["font"]["large"]["font"], self.config["font"]["large"]["size"]
        )
        self.font_normal = pygame.font.Font(
            self.config["font"]["normal"]["font"], self.config["font"]["normal"]["size"]
        )
        self.font_small = pygame.font.Font(
            self.config["font"]["small"]["font"], self.config["font"]["small"]["size"]
        )

    def read_cfg(self) -> typing.Dict:
        with open("./cfg/gogh.json") as f:
            config = json.load(f)
        return config

    @property
    def tile_width(self) -> int:
        return self.game_screen.get_width() // 10

    @property
    def tile_height(self) -> int:
        return self.game_screen.get_height() // 20

    def draw_game(self, active: np.ndarray, landed: np.ndarray) -> None:
        """
        Draws the game (board)
        """
        # self.main_screen.fill((0, 0, 0))
        # pygame.display.update()
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
        if self.config["grid"]["game"]:
            for x in range(0, self.game_screen.get_width(), self.tile_width):
                pygame.draw.line(
                    self.game_screen,
                    self.border_color,
                    (x, 0),
                    (x, self.game_screen.get_height()),
                )
            for y in range(0, self.game_screen.get_height(), self.tile_height):
                pygame.draw.line(
                    self.game_screen,
                    self.border_color,
                    (0, y),
                    (self.game_screen.get_width(), y),
                )
        self.main_screen.blit(self.game_screen, (0, 0))
        pygame.display.update(
            0, 0, self.game_screen.get_width(), self.game_screen.get_height()
        )

    def draw_preview(
        self,
        tetromino: typing.Union[
            tetrominos.I,
            tetrominos.J,
            tetrominos.L,
            tetrominos.O,
            tetrominos.S,
            tetrominos.T,
            tetrominos.Z,
        ],
    ) -> None:
        """
        Draws the preview of the next tetromino
        """
        self.preview_screen.fill(self.background_color)
        if tetromino.mask.shape[0] == 3:
            left_padding = self.tile_width // 2
        elif tetromino.mask.shape[0] == 2:
            left_padding = self.tile_width
        else:
            left_padding = 0
        top_padding = self.tile_height // 2
        for (y, x), value in np.ndenumerate(tetromino.mask):
            if value != 0:
                pygame.draw.rect(
                    self.preview_screen,
                    self.color_map[value],
                    pygame.Rect(
                        x * self.tile_width + left_padding,
                        y * self.tile_height + top_padding,
                        self.tile_width,
                        self.tile_height,
                    ),
                )
        if self.config["grid"]["preview"]:
            for x in range(0, self.preview_screen.get_width(), self.tile_width):
                pygame.draw.line(
                    self.preview_screen,
                    self.border_color,
                    (x, 0),
                    (x, self.preview_screen.get_height()),
                )
            for y in range(0, self.preview_screen.get_height(), self.tile_height):
                pygame.draw.line(
                    self.preview_screen,
                    self.border_color,
                    (0, y),
                    (self.preview_screen.get_width(), y),
                )
        self.main_screen.blit(self.preview_screen, (self.game_screen.get_width(), 0))
        pygame.display.update(
            self.game_screen.get_width(),
            0,
            self.preview_screen.get_width(),
            self.preview_screen.get_height(),
        )

    def draw_level(self, level: int) -> None:
        text_caption = self.font_normal.render("level:", True, (255, 255, 255))
        text_level = self.font_large.render(str(level), True, (255, 255, 255))
        self.level_screen.fill(self.background_color)
        self.level_screen.blit(text_caption, (0, 0))
        self.level_screen.blit(
            text_level,
            (
                (self.level_screen.get_width() - text_level.get_width()) // 2,
                (self.level_screen.get_height() - text_level.get_height()) // 2,
            ),
        )
        self.main_screen.blit(
            self.level_screen,
            (self.game_screen.get_width(), self.preview_screen.get_height()),
        )
        pygame.display.update(
            self.game_screen.get_width(),
            self.preview_screen.get_height(),
            self.level_screen.get_width(),
            self.level_screen.get_height(),
        )

    def draw_score(self, score: int) -> None:
        text_caption = self.font_normal.render("score:", True, (255, 255, 255))
        text_score = self.font_large.render(str(score), True, (255, 255, 255))
        self.score_screen.fill(self.background_color)
        self.score_screen.blit(text_caption, (0, 0))
        self.score_screen.blit(
            text_score,
            (
                (self.score_screen.get_width() - text_score.get_width()) // 2,
                (self.score_screen.get_height() - text_score.get_height()) // 2,
            ),
        )
        self.main_screen.blit(
            self.score_screen,
            (
                self.game_screen.get_width(),
                self.preview_screen.get_height() + self.level_screen.get_height(),
            ),
        )
        pygame.display.update(
            self.game_screen.get_width(),
            self.preview_screen.get_height() + self.level_screen.get_height(),
            self.level_screen.get_width(),
            self.level_screen.get_height(),
        )
