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

    def spawn_tetromino(self, type):
        self.current_tetromino = tetrominos.create_instance(type)
        self.place_tetromino()

    def place_tetromino(self):
        tetromino_mask = self.current_tetromino.mask
        x, y = self.current_tetromino.cords

        # Check if the Tetromino can be placed on the grid
        if self.is_valid_placement(x, y):
            self.active[y:y+self.current_tetromino.height,x:x+self.current_tetromino.width] += tetromino_mask[self.current_tetromino.top:self.current_tetromino.bottom+1,self.current_tetromino.left:self.current_tetromino.right+1]

    def is_valid_placement(self, x, y):
        if x  >= 0 - self.current_tetromino.left and x  < self.width-self.current_tetromino.right:
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
        