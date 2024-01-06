import numpy as np


class Base():
    def __init__(self, mask, cords, symbol):
        self.mask = np.array(mask, dtype=int)
        self.cords = cords
        self.symbol = symbol
        self.static = False
        self.left = 0
        self.right = 0
        self.top = 0
        self.bottom = 0
        self.calculate_boundaries()

    def __str__(self):
        return np.array_str(self.mask)

    def rotate(self):
        self.mask = np.rot90(self.mask, k=1)
        self.calculate_boundaries()

    def move_left(self):
        self.cords[0] -= 1

    def move_right(self):
        self.cords[0] += 1

    def move_down(self):
        self.cords[1] += 1

    @property
    def x(self):
        return self.cords[0]
    
    @property
    def y(self):
        return self.cords[1]
    
    @property
    def width(self):
        return self.right - self.left + 1

    @property
    def height(self):
        return self.bottom - self.top + 1

    def calculate_boundaries(self):
        y_nonzero, x_nonzero = np.where(self.mask != 0)
        self.top, self.bottom = np.min(y_nonzero), np.max(y_nonzero)
        self.left, self.right = np.min(x_nonzero), np.max(x_nonzero)
        print(f"top:{self.top} bottom:{self.bottom} left:{self.left} right:{self.right}")


class I(Base):
    def __init__(self, x, y):
        super().__init__([[0, 0, 0, 0],
                          [73, 73, 73, 73],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0]], [x, y], "I")


class J(Base):
    def __init__(self, x, y):
        super().__init__([[74, 0, 0],
                          [74, 74, 74],
                          [0, 0, 0]], [x, y], "J")


class L(Base):
    def __init__(self, x, y):
        super().__init__([[0, 0, 76],
                          [76, 76, 76],
                          [0, 0, 0]], [x, y], "L")


class O(Base):
    def __init__(self, x, y):
        super().__init__([[79, 79],
                          [79, 79]], [x, y], "O")


class S(Base):
    def __init__(self, x, y):
        super().__init__([[0, 83, 83],
                          [83, 83, 0],
                          [0, 0, 0]], [x, y], "S")


class T(Base):
    def __init__(self, x, y):
        super().__init__([[0, 84, 0],
                          [84, 84, 84],
                          [0, 0, 0]], [x, y], "T")


class Z(Base):
    def __init__(self, x, y):
        super().__init__([[90, 90, 0],
                          [0, 90, 90],
                          [0, 0, 0]], [x, y], "Z")


def create_instance(name, x = 0, y = 0):
    name_upper = name.upper()
    if name_upper == "I":
        return I(x, y)
    elif name_upper == "J":
        return J(x, y)
    elif name_upper == "L":
        return L(x, y)
    elif name_upper == "O":
        return O(x, y)
    elif name_upper == "S":
        return S(x, y)
    elif name_upper == "T":
        return T(x, y)
    elif name_upper == "Z":
        return Z(x, y)
    else:
        raise ValueError(f"{name} is not valid tetromino type")
