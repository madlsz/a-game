import numpy as np


class Base():
    def __init__(self, mask, cords, pivot = (1, 1)):
        self.mask = np.array(mask, dtype=int)
        self.cords = cords
        self.static = False
        self.left = 0
        self.right = 0
        self.top = 0
        self.bottom = 0
        self.pivot = pivot
        self.calculate_boundaries()


    def __str__(self):
        return np.array_str(self.mask)


    def rotate(self, k = 1):
        self.mask = np.rot90(self.mask, k)
        self.calculate_boundaries()


    def move_left(self):
        self.cords[0] -= 1


    def move_right(self):
        self.cords[0] += 1


    def move_down(self):
        self.cords[1] += 1
    

    def move_up(self):
        self.cords[1] -= 1


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
        # print(f"top:{self.top} bottom:{self.bottom} left:{self.left} right:{self.right}")


    # distances from the pivot to each side
    # the pivot will be externally treated as the 0,0 point,
    # so we need distances to calculate collisions
    @property
    def left_distance(self):
        return abs(self.left - self.pivot[0])


    @property
    def right_distance(self):
        return abs(self.right - self.pivot[0])


    @property
    def top_distance(self):
        return abs(self.top - self.pivot[1])


    @property
    def bottom_distance(self):
        return abs(self.bottom - self.pivot[1])


class I(Base):
    def __init__(self, x, y):
        super().__init__([[0, 0, 0, 0],
                          [73, 73, 73, 73],
                          [0, 0, 0, 0],
                          [0, 0, 0, 0]], [x, y - 1])
    
    def rotate(self, k = 1):
        self.mask = self.mask.T
        self.calculate_boundaries()


class J(Base):
    def __init__(self, x, y):
        super().__init__([[74, 0, 0],
                          [74, 74, 74],
                          [0, 0, 0]], [x, y])


class L(Base):
    def __init__(self, x, y):
        super().__init__([[0, 0, 76],
                          [76, 76, 76],
                          [0, 0, 0]], [x, y])


class O(Base):
    def __init__(self, x, y):
        super().__init__([[79, 79],
                          [79, 79]], [x, y])
        
    def rotate(self, k = 1):
        pass


class S(Base):
    def __init__(self, x, y):
        super().__init__([[0, 83, 83],
                          [83, 83, 0],
                          [0, 0, 0]], [x, y])


class T(Base):
    def __init__(self, x, y):
        super().__init__([[0, 84, 0],
                          [84, 84, 84],
                          [0, 0, 0]], [x, y])


class Z(Base):
    def __init__(self, x, y):
        super().__init__([[90, 90, 0],
                          [0, 90, 90],
                          [0, 0, 0]], [x, y])


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
