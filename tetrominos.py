import numpy as np


class Base:
    def __init__(self, mask, cords):
        self.mask = np.array(mask, dtype=str)
        self.cords = cords

    def __str__(self):
        return np.array_str(self.mask)

    def rotate(self):
        self.mask = np.rot90(self.mask, k=-1)

    def move_left(self):
        self.cords[0] -= 1

    def move_right(self):
        self.cords[0] += 1

    def move_down(self):
        self.cords[1] -= 1

    # def rotate_clockwise(self):
    #     self.mask = np.rot90(self.mask, k=-1)

    # def rotate_counterclockwise(self):
    #     self.mask = np.rot90(self.mask, k=1)


class I(Base):
    def __init__(self, x = 0, y = 0):
        super().__init__([["I", "I", "I", "I"]], [x, y])


class J(Base):
    def __init__(self, x = 0, y = 0):
        super().__init__([["J", "0", "0"],
                          ["J", "J", "J"]], [x, y])


class L(Base):
    def __init__(self, x = 0, y = 0):
        super().__init__([["0", "0", "L"],
                          ["L", "L", "L"]], [x, y])


class O(Base):
    def __init__(self, x = 0, y = 0):
        super().__init__([["O", "O"],
                          ["O", "O"]], [x, y])


class S(Base):
    def __init__(self, x = 0, y = 0):
        super().__init__([["0", "S", "S"],
                          ["S", "S", "0"]], [x, y])


class T(Base):
    def __init__(self, x = 0, y = 0):
        super().__init__([["0", "T", "0"],
                          ["T", "T", "T"]], [x, y])


class Z(Base):
    def __init__(self, x = 0, y = 0):
        super().__init__([["Z", "Z", "0"],
                          ["0", "Z", "Z"]], [x, y])


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
