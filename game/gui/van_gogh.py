import pygame
import numpy as np
from collections import defaultdict
import json
import typing

from game import tetrominos
from game.gui.button import Button


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

        self.tile_height = self.game_screen.get_height() // 20
        self.tile_width = self.game_screen.get_width() // 10

        self.preview_screen = pygame.Surface(
            (self.tile_width * 4, self.tile_height * 4)
        )
        self.score_screen = pygame.Surface((self.tile_width * 4, self.tile_height * 3))
        self.level_screen = pygame.Surface((self.tile_width * 4, self.tile_height * 3))
        self.lines_screen = pygame.Surface((self.tile_width * 4, self.tile_height * 3))
        self.button_screen = pygame.Surface(
            (
                self.tile_width * 4,
                screen.get_height() - self.tile_height * 13,
            )
        )

        self.font_large = pygame.font.Font(
            self.config["font"]["large"]["font"], self.config["font"]["large"]["size"]
        )
        self.font_normal = pygame.font.Font(
            self.config["font"]["normal"]["font"], self.config["font"]["normal"]["size"]
        )
        self.font_small = pygame.font.Font(
            self.config["font"]["small"]["font"], self.config["font"]["small"]["size"]
        )

        self.old_board = None

    def read_cfg(self) -> typing.Dict:
        with open("./cfg/gogh.json") as f:
            config = json.load(f)
        return config

    def draw_pause(self):
        text = self.font_large.render("GAME PAUSED", True, (255, 255, 255))
        self.game_screen.blit(
            text,
            (
                (self.game_screen.get_width() - text.get_width()) // 2,
                (self.game_screen.get_height() - text.get_height()) // 2,
            ),
        )
        self.main_screen.blit(self.game_screen, (0, 0))
        pygame.display.update(
            0, 0, self.game_screen.get_width(), self.game_screen.get_height()
        )

    def draw_buttons(self, buttons: typing.List[Button]) -> None:
        self.button_screen.fill(self.config["background_color"]["buttons"])
        for i, button in enumerate(buttons):
            button.x = self.game_screen.get_width() + (
                (self.button_screen.get_width() - button.width) // 2
            )
            button.y = self.tile_height * 13 + button.height * i
            self.button_screen.blit(
                button.surface,
                (
                    (self.button_screen.get_width() - button.width) // 2,
                    button.height * i,
                ),
            )
        self.main_screen.blit(
            self.button_screen, (self.game_screen.get_width(), self.tile_height * 13)
        )
        pygame.display.update(
            self.game_screen.get_width(),
            self.tile_height * 13,
            self.button_screen.get_width(),
            self.button_screen.get_height(),
        )

    def draw_board(self, board: np.ndarray):
        """
        draws the board into self.game_screen
        """
        self.game_screen.fill(self.config["background_color"]["game"])
        for (y, x), value in np.ndenumerate(board):
            if value != 0:
                pygame.draw.rect(
                    self.game_screen,
                    self.color_map[value],
                    pygame.Rect(
                        x * self.tile_width + 2,
                        y * self.tile_height + 2,
                        self.tile_width - 4,
                        self.tile_height - 4,
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

    def draw_game(self, active: np.ndarray, landed: np.ndarray) -> None:
        """
        Draws the game (board)
        """
        # if not np.any((active != 0) & (landed != 0)):
        board = np.where(landed != 0, landed, active)

        if self.config["animate_line_clear"]:
            # check for removed lines
            if self.old_board is not None:
                # missing lines
                if np.sum(board) < np.sum(self.old_board):
                    lines_to_remove = []
                    for y in range(len(self.old_board)):
                        if np.all(self.old_board[y, :] != 0):
                            lines_to_remove.append(y)

                    left = [i for i in range(4, -1, -1)]
                    right = [i for i in range(5, 10)]
                    for x in range(len(left)):
                        for y in lines_to_remove:
                            self.old_board[y, left[x]] = 0
                            self.old_board[y, right[x]] = 0

                        self.draw_board(self.old_board)
                        pygame.time.wait(self.config["animate_line_speed"])

            self.old_board = board.copy()

        if self.config["ghost_piece"]:
            # calculate the span of the active tetromino
            tetromino_span_y = []
            for y in range(len(active)):
                if not np.all(active[y, :] == 0):
                    tetromino_span_y.append(y)
            tetromino_span_y_start = np.min(tetromino_span_y)
            tetromino_span_y_end = np.max(tetromino_span_y) + 1

            ghost = np.full((20, 10), 0, dtype=int)
            offset_y = tetromino_span_y_end - tetromino_span_y_start
            while tetromino_span_y_end + offset_y <= active.shape[0] and not np.any(
                (ghost != 0) & (board != 0)
            ):
                ghost = np.roll(active, offset_y, axis=0)
                offset_y += 1
            offset_y -= 1
            # add the ghost to the board
            if np.any((ghost != 0) & (board != 0)):
                offset_y -= 1
                ghost = np.full((20, 10), 0, dtype=int)
                ghost[
                    tetromino_span_y_start + offset_y : tetromino_span_y_end + offset_y,
                    :,
                ] = active[tetromino_span_y_start:tetromino_span_y_end, :]

            board = np.where(board != 0, board, ghost)

        self.draw_board(board)

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
        self.preview_screen.fill(self.config["background_color"]["preview"])
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
                        x * self.tile_width + 2 + left_padding,
                        y * self.tile_height + 2 + top_padding,
                        self.tile_width - 4,
                        self.tile_height - 4,
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
        self.level_screen.fill(self.config["background_color"]["level"])
        self.level_screen.blit(text_caption, (7, 0))
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
        self.score_screen.fill(self.config["background_color"]["score"])
        self.score_screen.blit(text_caption, (7, 0))
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

    def draw_lines(self, lines: int) -> None:
        text_caption = self.font_normal.render("lines:", True, (255, 255, 255))
        text_score = self.font_large.render(str(lines), True, (255, 255, 255))
        self.score_screen.fill(self.config["background_color"]["score"])
        self.score_screen.blit(text_caption, (7, 0))
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
                self.preview_screen.get_height()
                + self.level_screen.get_height()
                + self.score_screen.get_height(),
            ),
        )
        pygame.display.update(
            self.game_screen.get_width(),
            self.preview_screen.get_height()
            + self.level_screen.get_height()
            + self.score_screen.get_height(),
            self.level_screen.get_width(),
            self.level_screen.get_height(),
        )