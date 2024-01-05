import numpy as np
import pygame
import random

import tetrominos

class Game:
    def __init__(self, width = 10, height = 20):
        self.width = width
        self.height = height
        self.board = np.full((self.height, self.width), 0, dtype=int)

    def clear_board(self):
        self.board = np.full((self.height, self.width), 0, dtype=int)

    def __str__(self):
        return np.array_str(self.board)

    # def start(self):


    def spawn_tetromino(self, tetromino):
        self.current_tetromino = tetromino
        self.place_tetromino()

    def place_tetromino(self):
        tetromino_mask = self.current_tetromino.mask
        x, y = self.current_tetromino.cords

        # Check if the Tetromino can be placed on the grid
        if self.is_valid_placement(tetromino_mask, x, y):
            self.board[y:y+tetromino_mask.shape[0], x:x+tetromino_mask.shape[1]] += tetromino_mask

    def is_valid_placement(self, tetromino_mask, x, y):
        # Check for collisions with other pieces or out-of-bounds
        if (
            0 <= x < self.width - tetromino_mask.shape[1] + 1
            and 0 <= y < self.height - tetromino_mask.shape[0] + 1
        ):
            overlapping_cells = self.board[y:y+tetromino_mask.shape[0], x:x+tetromino_mask.shape[1]]
            return np.all((tetromino_mask == 0) | (overlapping_cells == 0))
        return False

    def move_tetromino_left(self):
        self.current_tetromino.move_left()
        self.place_tetromino()

    def move_tetromino_right(self):
        self.current_tetromino.move_right()
        self.place_tetromino()

    def rotate_tetromino(self):
        self.current_tetromino.rotate()
        self.place_tetromino()

    def move_tetromino_down(self):
        self.current_tetromino.move_down()
        self.place_tetromino()

    def clear_lines(self):
        # Implement line clearing logic
        pass

game = Game()
tetromino_names = ["I", "J", "L", "O", "S", "T", "Z"]
random_tetromino = tetrominos.create_instance(random.choice(tetromino_names))
game.spawn_tetromino(tetrominos.create_instance("O"))

game.move_tetromino_right()
game.move_tetromino_right()
game.move_tetromino_down()
game.move_tetromino_down()
game.move_tetromino_down()
game.clear_board()
game.move_tetromino_down()
# game.rotate_tetromino()
# game.move_tetromino_down()

print(game)