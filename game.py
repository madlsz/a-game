import numpy as np

import tetrominos


class Game:
    def __init__(self, width = 10, height = 20):
        self.width = width
        self.height = height
        self.active = np.full((self.height, self.width), 0, dtype=int)
        self.landed = np.full((self.height, self.width), 0, dtype=int)
        # self.landed[5,5] = 90

    def clear_active(self):
        self.active = np.full((self.height, self.width), 0, dtype=int)

    def clear_landed(self):
        self.landed = np.full((self.height, self.width), 0, dtype=int)

    def __str__(self):
        return np.array_str(self.active + self.landed)

    def spawn_tetromino(self, type):
        self.current_tetromino = tetrominos.create_instance(type)
        self.place_tetromino()

    def place_tetromino(self):
        tetromino_mask = self.current_tetromino.mask
        x, y = self.current_tetromino.cords

        # Check if the Tetromino can be placed on the grid
        if self.is_valid_placement(x, y):
            mask_height, mask_width = tetromino_mask.shape
            active_height, active_width = self.active.shape

            # Calculate the valid region to update
            y_start, y_end = max(0, y), min(active_height, y + mask_height)
            x_start, x_end = max(0, x), min(active_width, x + mask_width)

            # Update the valid region with the tetromino_mask
            self.active[y_start:y_end, x_start:x_end] += tetromino_mask[:y_end-y_start, :x_end-x_start]

    def is_valid_placement(self, x, y):
        if x - self.current_tetromino.left >= 0 and x + self.current_tetromino.right < self.width:
            if y + self.current_tetromino.top >= 0 and y + self.current_tetromino.bottom < self.height:
                return True 
            
        # TODO: check with static tiles
        print("invalid!")
        return False

    # after a successfull movement return True to reset the movement timeout
    def move_tetromino_left(self):
        if self.is_valid_placement(self.current_tetromino.x - 1, self.current_tetromino.y):
            self.current_tetromino.move_left()
        self.place_tetromino()
        return True

    def move_tetromino_right(self):
        if self.is_valid_placement(self.current_tetromino.x + 1, self.current_tetromino.y):
            self.current_tetromino.move_right()
        self.place_tetromino()
        return True

    def rotate_tetromino(self):
        self.current_tetromino.rotate()
        self.place_tetromino()
        return True

    def move_tetromino_down(self):
        if self.is_valid_placement(self.current_tetromino.x, self.current_tetromino.y + 1):
            self.current_tetromino.move_down()
        self.place_tetromino()
        return True

    # def clear_lines(self):
    #     # Implement line clearing logic
    #     pass
        