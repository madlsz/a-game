import numpy as np

import tile

class Base:
    def __init__(self, mask, cords, color, screen, symbol):
        self.screen = screen
        self.mask = np.array(mask, dtype=int)
        self.cords = cords
        self.color = color
        self.tiles = [tile.Tile(screen, 0,0,self.color), tile.Tile(screen, screen.get_width()/10,0, self.color)]
        self.symbol = symbol
        self.static = False

    def __str__(self):
        return np.array_str(self.mask)

    def rotate(self):
        self.mask = np.rot90(self.mask, k=-1)

    def move_left(self):
        self.cords[0] -= 1

    def move_right(self):
        self.cords[0] += 1

    def move_down(self):
        self.cords[1] += 1

    def move_x(self, x):
        for tile in self.tiles:
            if not (tile.x + tile.width + x <= self.screen.get_width() and tile.x + x >= 0):
                return
        for tile in self.tiles:
            tile.move_x(x)


class I(Base):
    def __init__(self, screen, x, y):
        super().__init__([[1, 1, 1, 1]], [x, y], (55, 255, 255), screen, "I")


class J(Base):
    def __init__(self, screen, x, y):
        super().__init__([[1, 0, 0],
                          [1, 1, 1]], [x, y], (51, 51, 255), screen, "J")


class L(Base):
    def __init__(self, screen, x, y):
        super().__init__([[0, 0, 1],
                          [1, 1, 1]], [x, y], (255, 128, 0), screen, "L")


class O(Base):
    def __init__(self, screen, x, y):
        super().__init__([[1, 1],
                          [1, 1]], [x, y], (255, 255, 51), screen, "O")


class S(Base):
    def __init__(self, screen, x, y):
        super().__init__([[0, 1, 1],
                          [1, 1, 0]], [x, y], (0, 255, 0), screen, "S")


class T(Base):
    def __init__(self, screen, x, y):
        super().__init__([[0, 1, 0],
                          [1, 1, 1]], [x, y], (255, 0, 255), screen, "T")


class Z(Base):
    def __init__(self, screen, x, y):
        super().__init__([[1, 1, 0],
                          [0, 1, 1]], [x, y], (255, 51, 51), screen, "Z")


def create_instance(name, screen, x = 0, y = 0):
    name_upper = name.upper()
    if name_upper == "I":
        return I(screen, x, y)
    elif name_upper == "J":
        return J(screen, x, y)
    elif name_upper == "L":
        return L(screen, x, y)
    elif name_upper == "O":
        return O(screen, x, y)
    elif name_upper == "S":
        return S(screen, x, y)
    elif name_upper == "T":
        return T(screen, x, y)
    elif name_upper == "Z":
        return Z(screen, x, y)
    else:
        raise ValueError(f"{name} is not valid tetromino type")
