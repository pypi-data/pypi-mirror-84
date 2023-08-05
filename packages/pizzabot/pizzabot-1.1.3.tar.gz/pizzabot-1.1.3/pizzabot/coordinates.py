from math import sqrt


class PizzabotCoordinate:
    """
    A class to represent a coordinate.

    ...

    Attributes
    ----------
    points : list
        List of integers that encode a coordinate

    Methods
    -------
    __len__():
        Returns the number of dimensions of coordinate

    _check_len():
        When preforming math on coordinate, make sure they share dimensions.

    __abs__():
        Returns the size of the coordinate

    __iadd__():
        Returns the sum of coordinates

    __sub__():
        Returns the difference of coordinates

    __sub__():
        Returns true if the coordinates are the same
    """

    def __init__(self, *argv):
        self.points = []
        for arg in argv:
            if isinstance(arg, int):
                self.points.append(arg)
            else:
                raise ValueError(
                    "ValueError exception thrown, non-int passed to PizzabotCoordinate",
                    argv,
                )

    def __len__(self):
        return len(self.points)

    def _check_len(self, other):
        if len(self) != len(other):
            raise TypeError(
                "TypeError exception thrown, PizzabotCoordinate points dimensions do not match",
                self.points,
                other.point,
            )

    def __abs__(self):
        sum_of_squares = 0
        for sp in self.points:
            sum_of_squares += sp * sp
        return sqrt(sum_of_squares)

    def __iadd__(self, other):
        added = []
        self._check_len(other)
        for sp, op in zip(self.points, other.points):
            added.append(sp + op)
        return PizzabotCoordinate(*added)

    def __sub__(self, other):
        delta = []
        self._check_len(other)
        for sp, op in zip(self.points, other.points):
            delta.append(sp - op)
        return PizzabotCoordinate(*delta)

    def __eq__(self, other):
        delta = []
        self._check_len(other)
        for sp, op in zip(self.points, other.points):
            if sp != op:
                return False
        return True
