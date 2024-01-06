import numpy as np


class Game:
    def __init__(self, width = 10, height = 20):
        self.width = width
        self.height = height
        self.active = np.full((self.height, self.width), 0, dtype=int)
        self.landed = np.full((self.height, self.width), 0, dtype=int)
        self.landed[5,5] = 90

    def clear_active(self):
        self.active = np.full((self.height, self.width), 0, dtype=int)

    def clear_landed(self):
        self.landed = np.full((self.height, self.width), 0, dtype=int)

    def __str__(self):
        return np.array_str(self.active + self.landed)

    def spawn_tetromino(self, tetromino):
        self.current_tetromino = tetromino
        self.place_tetromino()

    def place_tetromino(self):
        tetromino_mask = self.current_tetromino.mask
        x, y = self.current_tetromino.cords

        # Check if the Tetromino can be placed on the grid
        if self.is_valid_placement(tetromino_mask, x, y):
            self.active[y:y+tetromino_mask.shape[0], x:x+tetromino_mask.shape[1]] += tetromino_mask

    def is_valid_placement(self, tetromino_mask, x, y):
        # Check for collisions with other pieces or out-of-bounds
        if 0 <= x < self.width - tetromino_mask.shape[1] + 1:
            if 0 <= y < self.height - tetromino_mask.shape[0] + 1:
                overlapping_cells = self.active[y:y+tetromino_mask.shape[0], x:x+tetromino_mask.shape[1]]
                return np.all((tetromino_mask == 0) | (overlapping_cells == 0))
        return False

    # after a successfull movement return True to reset the movement timeout
    def move_tetromino_left(self):
        if self.is_valid_placement(self.current_tetromino.mask, self.current_tetromino.x - 1, self.current_tetromino.y):
            self.current_tetromino.move_left()
        self.place_tetromino()
        return True

    def move_tetromino_right(self):
        if self.is_valid_placement(self.current_tetromino.mask, self.current_tetromino.x + 1, self.current_tetromino.y):
            self.current_tetromino.move_right()
        self.place_tetromino()
        return True

    def rotate_tetromino(self):
        self.current_tetromino.rotate()
        self.place_tetromino()
        return True

    def move_tetromino_down(self):
        if self.is_valid_placement(self.current_tetromino.mask, self.current_tetromino.x, self.current_tetromino.y + 1):
            self.current_tetromino.move_down()
        self.place_tetromino()
        return True

    # def clear_lines(self):
    #     # Implement line clearing logic
    #     pass
        