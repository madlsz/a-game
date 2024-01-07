import numpy as np

import tetrominos


class Game:
    def __init__(self, width = 10, height = 20):
        self.width = width
        self.height = height
        self.active = np.full((self.height, self.width), 0, dtype=int)
        self.landed = np.full((self.height, self.width), 0, dtype=int)
        self.score = 0


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
            self.clear_active()
            # Adjust the tetromino_mask slice dimensions based on top, left, height, and width
            tetromino_slice = tetromino_mask[self.current_tetromino.top:self.current_tetromino.bottom+1,self.current_tetromino.left:self.current_tetromino.right+1]

            # Update the valid region with the adjusted tetromino_mask slice
            self.active[y-self.current_tetromino.top_distance:y + self.current_tetromino.bottom_distance+1, x-self.current_tetromino.left_distance:x+self.current_tetromino.right_distance+1] = tetromino_slice
            return True

        else:
            return False


    def is_valid_placement(self, x, y):
        if x - self.current_tetromino.left_distance >= 0 and x + self.current_tetromino.right_distance < self.width:
            if y - self.current_tetromino.top_distance >= 0 and y + self.current_tetromino.bottom_distance < self.height:
                return True
        return False
    

    def check_for_overlaps(self):
        return not np.any((self.active != 0) & (self.landed != 0))

    # after a successfull movement return True to reset the movement timeout
    def move_tetromino_left(self):
        if self.is_valid_placement(self.current_tetromino.x - 1, self.current_tetromino.y):
            self.current_tetromino.move_left()
            self.place_tetromino()
            if self.check_for_overlaps():
                return True
            else:
                self.current_tetromino.move_right()
                self.place_tetromino()
        return False


    def move_tetromino_right(self):
        if self.is_valid_placement(self.current_tetromino.x + 1, self.current_tetromino.y):
            self.current_tetromino.move_right()
            self.place_tetromino()
            if self.check_for_overlaps():
                return True
            else:
                self.current_tetromino.move_left()
                self.place_tetromino()
        return False


    def rotate_tetromino(self):
        self.current_tetromino.rotate()
        if self.is_valid_placement(self.current_tetromino.x, self.current_tetromino.y):
            self.place_tetromino()
            if self.check_for_overlaps():
                return True
            else:
                self.current_tetromino.rotate(-1)
                self.place_tetromino()
                return False
        else:
            self.current_tetromino.rotate(-1)
            return False


    def move_tetromino_down(self):
        if self.is_valid_placement(self.current_tetromino.x, self.current_tetromino.y + 1):
            self.current_tetromino.move_down()
            self.place_tetromino()
            if self.check_for_overlaps():
                return True
            else:
                self.current_tetromino.move_up()
                self.place_tetromino()
        return False
    
    def push_to_landed(self):
        self.landed += self.active
        self.clear_active()
        self.current_tetromino = None

        self.clear_lines()


    def clear_lines(self):
        for y in range(len(self.landed)):
            if np.all(self.landed[y, :] != 0):
                self.landed[1:y+1, :] = self.landed[0:y, :]
                self.landed[0, :] = 0
                self.score += 1
        print(self.score)
        