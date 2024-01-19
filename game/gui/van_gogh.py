import pygame
import numpy as np
from collections import defaultdict
import json
import typing

from game.models import tetrominos
from game.gui.button import Button


class VanGogh:
    """
    Responsible for rendering the game scene
    """

    def __init__(self, screen: pygame.Surface) -> None:
        self.main_screen = screen
        self.config = self.read_cfg()
        self.main_screen.fill(self.config["background_color"]["game"])
        pygame.display.update()
        self.color_map = defaultdict(lambda: self.config["default_tile_color"])
        for tile in self.config["tiles_colors"]:
            self.color_map[int(tile)] = self.config["tiles_colors"][tile]
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

        self.board = None
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

    def draw_buttons(self, buttons: typing.List[Button], display_buttons: bool) -> None:
        self.button_screen.fill(self.config["background_color"]["buttons"])
        if display_buttons:
            for i, button in enumerate(buttons):
                button.x = self.game_screen.get_width() + (
                    (self.button_screen.get_width() - button.width) // 2
                )
                button.y = self.tile_height * 13 + button.height * i
                self.button_screen.blit(
                    button.surface,
                    (
                        (self.button_screen.get_width() - button.width) // 2,
                        button.height * i * 1.3,
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
        Displays the board on the self.game_screen
        """
        self.game_screen.fill(self.config["background_color"]["game"])
        for (y, x), value in np.ndenumerate(board[2:, :]):
            if value != 0:
                if value != 1 or self.config["ghost_piece_style"] == "solid":
                    pygame.draw.rect(
                        self.game_screen,
                        self.color_map[value],
                        pygame.Rect(
                            x * self.tile_width + self.tile_width * 0.065,
                            y * self.tile_height + self.tile_height * 0.065,
                            self.tile_width - 2 * self.tile_width * 0.065,
                            self.tile_height - 2 * self.tile_height * 0.065,
                        ),
                    )
                elif value == 1 and self.config["ghost_piece_style"] == "outline":
                    pygame.draw.rect(
                        self.game_screen,
                        (255, 255, 255),
                        pygame.Rect(
                            x * self.tile_width + self.tile_width * 0.065,
                            y * self.tile_height + self.tile_height * 0.065,
                            self.tile_width - 2 * self.tile_width * 0.065,
                            self.tile_height - 2 * self.tile_height * 0.065,
                        ),
                    )
                    pygame.draw.rect(
                        self.game_screen,
                        self.config["background_color"]["game"],
                        pygame.Rect(
                            x * self.tile_width + self.tile_width * 0.075,
                            y * self.tile_height + self.tile_height * 0.075,
                            self.tile_width - 2 * self.tile_width * 0.09,
                            self.tile_height - 2 * self.tile_height * 0.09,
                        ),
                    )
        self.main_screen.blit(self.game_screen, (0, 0))
        pygame.display.update(
            0, 0, self.game_screen.get_width(), self.game_screen.get_height()
        )

    def animate_line_clear(self) -> None:
        """
        Displays the line clear animation
        """
        # check for removed lines
        if self.old_board is not None:
            # missing lines
            if np.sum(self.board) < np.sum(self.old_board):
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

        self.old_board = self.board.copy()

    def display_ghost(self, active: np.ndarray, landed: np.ndarray) -> None:
        """
        Adds the ghost piece to the self.board
        """
        # Calculate the span of the active tetromino
        tetromino_span_y = np.where(active.sum(axis=1) > 0)[0]
        tetromino_span_y_end = tetromino_span_y.max() + 1

        # Calculate the offset based on the lowest position for the ghost piece
        offset_y = 0
        while tetromino_span_y_end + offset_y < self.board.shape[0] and not np.any(
            (landed != 0) & (np.roll(active, offset_y + 1, axis=0) != 0)
        ):
            offset_y += 1

        # Create the ghost piece at the correct position
        ghost = np.roll(active, offset_y, axis=0)

        # Add the ghost to the board
        ghost = np.where(ghost != 0, 1, 0)
        self.board = np.where(self.board != 0, self.board, ghost)

    def draw_game(self, active: np.ndarray, landed: np.ndarray) -> None:
        """
        Combines active and landed, adds effects and animations, after that calls self.draw_board
        """
        self.board = np.where(landed != 0, landed, active)

        if self.config["animate_line_clear"]:
            self.animate_line_clear()

        if self.config["ghost_piece"]:
            self.display_ghost(active, landed)

        self.draw_board(self.board)

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
        if self.config["preview"]:
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
                            x * self.tile_width
                            + self.tile_width * 0.065
                            + left_padding,
                            y * self.tile_height
                            + self.tile_height * 0.065
                            + top_padding,
                            self.tile_width - 2 * self.tile_width * 0.065,
                            self.tile_height - 2 * self.tile_height * 0.065,
                        ),
                    )
        self.main_screen.blit(self.preview_screen, (self.game_screen.get_width(), 0))
        pygame.display.update(
            self.game_screen.get_width(),
            0,
            self.preview_screen.get_width(),
            self.preview_screen.get_height(),
        )

    def draw_level(self, level: int) -> None:
        """
        Displays current level
        """
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
        """
        Displays total score
        """
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
        """
        Displays cleared lines counter
        """
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
