"""Vector and Matrix classes to support the :func:`felt.estimate.estimate`
function."""

class Vector:
    """A one-dimensional array of numbers.

    Args:
        values: a list of numbers
    """

    def __init__(self, values):
        self._values = list(values)

    def __iter__(self):
        return iter(self._values)

    def __len__(self):
        return len(self._values)

    def __repr__(self):
        return f'Vector({self._values})'

    def __str__(self):
        return  f'Vector({[round(v, 2) for v in self._values]})'

    def __mul__(self, other):
        if isinstance(other, Vector):
            if len(self) != len(other):
                raise ValueError
            return Vector([a * b for a, b in zip(self, other)])
        if isinstance(other, (int, float)):
            return Vector([a * other for a in self])
        raise ValueError()

    def __matmul__(self, other):
        if not isinstance(other, Vector):
            raise ValueError
        return sum(self * other)

    def __getitem__(self, i):
        return self._values[i]

    def __setitem__(self, index, value):
        if not isinstance(index, int):
            raise ValueError("Expected index to be an int.")
        self._values[index] = value

    def equals(self, other):
        """Check whether two Vectors are equal to each other."""
        if not isinstance(other, Vector):
            return False
        return self._values == list(other)

    @staticmethod
    def ones(size):
        """Make a vector filled with ones."""
        return Vector([1.0] * size)


class Matrix:
    """A two-dimensional matrix filled with numbers

    Args:
        rows: a list of lists. Each nested list must be of equal length.

    """
    def __init__(self, rows):
        rows = [Vector(row) for row in rows]
        if len(set(len(v) for v in rows)) != 1:
            raise ValueError("rows are not of equal length")
        self.shape = len(rows), len(rows[0])
        self._rows = rows

    def __getitem__(self, i):
        return self._rows[i]

    def __iter__(self):
        return iter(self._rows)

    def __repr__(self):
        return f'Matrix({self._rows})'

    def __str__(self):
        rounded = [[round(v, 2) for v in row] for row in self]
        return f'Matrix({rounded})'

    def __matmul__(self, vec):
        if not isinstance(vec, Vector):
            raise ValueError("Matrix multiplication supported for only Vectors")
        if self.shape[1] != len(vec):
            raise ValueError("Vector size does not match")

        return Vector([row @ vec for row in self])
