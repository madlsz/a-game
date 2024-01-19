import numpy as np
import typing


class Base:
    def __init__(
        self,
        mask: typing.List[typing.List[int]],
        coords: typing.Tuple[int, int],
        pivot: typing.Tuple[int, int] = (1, 1),
    ) -> None:
        self.x, self.y = coords
        self.mask = np.array(mask, dtype=int)
        self.coords = coords
        self.static = False
        self.left = 0
        self.right = 0
        self.top = 0
        self.bottom = 0
        self.pivot = pivot
        self.calculate_boundaries()

    def __str__(self) -> str:
        return np.array_str(self.mask)

    def rotate(self, clockwise: bool) -> None:
        k = 1 if clockwise else -1
        self.mask = np.rot90(self.mask, k)
        self.calculate_boundaries()

    def move(self, x: int, y: int) -> None:
        self.x += x
        self.y += y

    @property
    def width(self) -> int:
        return self.right - self.left + 1

    @property
    def height(self) -> int:
        return self.bottom - self.top + 1

    # needs to be called after each rotation to provide data needed to calculate distances from the pivot
    def calculate_boundaries(self) -> None:
        y_nonzero, x_nonzero = np.where(self.mask != 0)
        self.top, self.bottom = np.min(y_nonzero), np.max(y_nonzero)
        self.left, self.right = np.min(x_nonzero), np.max(x_nonzero)

    # distances from the pivot to each side
    # the pivot will be externally treated as the 0,0 point,
    # so we need distances to calculate collisions
    @property
    def left_distance(self) -> int:
        return abs(self.left - self.pivot[0])

    @property
    def right_distance(self) -> int:
        return abs(self.right - self.pivot[0])

    @property
    def top_distance(self) -> int:
        return abs(self.top - self.pivot[1])

    @property
    def bottom_distance(self) -> int:
        return abs(self.bottom - self.pivot[1])


class I(Base):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(
            [[0, 0, 0, 0], [73, 73, 73, 73], [0, 0, 0, 0], [0, 0, 0, 0]], [x, y - 1]
        )

    def rotate(self, clockwise: bool):
        self.mask = self.mask.T
        self.calculate_boundaries()


class J(Base):
    def __init__(self, x: int, y: int) -> None:
        super().__init__([[74, 0, 0], [74, 74, 74], [0, 0, 0]], [x, y])


class L(Base):
    def __init__(self, x: int, y: int) -> None:
        super().__init__([[0, 0, 76], [76, 76, 76], [0, 0, 0]], [x, y])


class O(Base):
    def __init__(self, x: int, y: int) -> None:
        super().__init__([[79, 79], [79, 79]], [x + 1, y])

    def rotate(self, clockwise: bool) -> None:
        pass


class S(Base):
    def __init__(self, x: int, y: int) -> None:
        super().__init__([[0, 83, 83], [83, 83, 0], [0, 0, 0]], [x, y])


class T(Base):
    def __init__(self, x: int, y: int) -> None:
        super().__init__([[0, 84, 0], [84, 84, 84], [0, 0, 0]], [x, y])


class Z(Base):
    def __init__(self, x: int, y: int) -> None:
        super().__init__([[90, 90, 0], [0, 90, 90], [0, 0, 0]], [x, y])


def create_instance(name, x: int = 0, y: int = 0) -> typing.Union[I, J, L, O, S, T, Z]:
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
