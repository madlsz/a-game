import numpy as np


class Base:
    def __init__(self, mask, cords, color):
        self.mask = np.array(mask, dtype=int)
        self.cords = cords
        self.color = color

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

    # def rotate_clockwise(self):
    #     self.mask = np.rot90(self.mask, k=-1)

    # def rotate_counterclockwise(self):
    #     self.mask = np.rot90(self.mask, k=1)


class I(Base):
    def __init__(self, x = 0, y = 0):
        super().__init__([[1, 1, 1, 1]], [x, y], (55, 255, 255))


class J(Base):
    def __init__(self, x = 0, y = 0):
        super().__init__([[1, 0, 0],
                          [1, 1, 1]], [x, y], (51, 51, 255))


class L(Base):
    def __init__(self, x = 0, y = 0):
        super().__init__([[0, 0, 1],
                          [1, 1, 1]], [x, y], (255, 128, 0))


class O(Base):
    def __init__(self, x = 0, y = 0):
        super().__init__([[1, 1],
                          [1, 1]], [x, y], (255, 255, 51))


class S(Base):
    def __init__(self, x = 0, y = 0):
        super().__init__([[0, 1, 1],
                          [1, 1, 0]], [x, y], (0, 255, 0))


class T(Base):
    def __init__(self, x = 0, y = 0):
        super().__init__([[0, 1, 0],
                          [1, 1, 1]], [x, y], (255, 0, 255))


class Z(Base):
    def __init__(self, x = 0, y = 0):
        super().__init__([[1, 1, 0],
                          [0, 1, 1]], [x, y], (255, 51, 51))


def create_instance(name, x=0, y=0):
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
