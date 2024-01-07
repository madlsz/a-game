import numpy as np

import tetrominos


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

    def spawn_tetromino(self, type, x = 0, y = 0):
        self.current_tetromino = tetrominos.create_instance(type, x, y)
        self.place_tetromino()

    def place_tetromino(self):
        tetromino_mask = self.current_tetromino.mask
        x, y = self.current_tetromino.cords

        # Check if the Tetromino can be placed on the grid
        if self.is_valid_placement(x, y):
            print("valid placement")
            # Calculate the valid region to update
            y_start, y_end = max(0, y), min(self.height, y + tetromino_mask.shape[0])
            x_start, x_end = max(0, x), min(self.width, x + tetromino_mask.shape[1])

            # Update only the valid region with the tetromino_mask
            self.active[y_start:y_end, x_start:x_end] += tetromino_mask[:y_end - y_start, :x_end - x_start]
        else:
            print("invalid placement")


    def is_valid_placement(self, x, y):
        if x - self.current_tetromino.left_distance >= 0 and x + self.current_tetromino.right_distance < self.width:
            if y - self.current_tetromino.top_distance >= 0 and y + self.current_tetromino.bottom_distance < self.height:
                return True 
            
        # TODO: check with static tiles
        # print("invalid!")
        return False

    # after a successfull movement return True to reset the movement timeout
    def move_tetromino_left(self):
        if self.is_valid_placement(self.current_tetromino.x - 1, self.current_tetromino.y):
            self.current_tetromino.move_left()
            self.clear_active()
            self.place_tetromino()
            return True
        return False

    def move_tetromino_right(self):
        if self.is_valid_placement(self.current_tetromino.x + 1, self.current_tetromino.y):
            self.current_tetromino.move_right()
            self.clear_active()
            self.place_tetromino()
            return True
        return False

    def rotate_tetromino(self):
        self.current_tetromino.rotate()
        if self.is_valid_placement(self.current_tetromino.x, self.current_tetromino.y):
            self.clear_active()
            self.place_tetromino()
            return True
        else:
            self.current_tetromino.rotate(-1)
            return False

    def move_tetromino_down(self):
        if self.is_valid_placement(self.current_tetromino.x, self.current_tetromino.y + 1):
            self.current_tetromino.move_down()
            self.clear_active()
            self.place_tetromino()
            return True
        return False

    # def clear_lines(self):
    #     # Implement line clearing logic
    #     pass
        