import numpy as np

import tetrominos

class Game:
    def __init__(self, width = 10, height = 20):
        self.width = width
        self.height = height
        self.board = None
        self.clear_board()

    def clear_board(self):
        self.board = np.full((self.height, self.width),"0" ,dtype=str)

    def __str__(self):
        return np.array_str(self.board)

    def start(self):
        t = tetrominos.create_instance("z")
        self.insert_tetromino(t)

    def insert_tetromino(self, tetromino):
            tetromino_height, tetromino_width = tetromino.mask.shape
            x, y = tetromino.cords
            self.board[y:y+tetromino_height, x:x+tetromino_width] = np.where(tetromino.mask != "0", tetromino.mask, self.board[y:y+tetromino_height, x:x+tetromino_width])