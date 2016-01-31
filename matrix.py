# coding = utf-8

import numpy as np


class Matrix(object):
    _matrix = None
    _det = None

    def __init__(self, matrix):
        self._matrix = np.matrix([
            list(map(np.float64, row))
            for row in matrix
        ])
        self._det = np.linalg.det(matrix)

    def item(self, row, col):
        return (-1) ** (row + col) * self.minor(row, col) / self._det

    def minor(self, row, col):
        sm = self._submatrix(row, col)
        return np.linalg.det(sm)

    def _submatrix(self, row, col):
        arr = self._matrix
        return arr[np.array(list(range(row-1)) + list(range(row, arr.shape[0])))[:, np.newaxis],
                   np.array(list(range(col-1)) + list(range(col, arr.shape[1])))]
