# coding = utf-8

import cmath

from errors import CalculationError
from params import Params

beta = {
    1: 0.,
    2: 0.,
}

omega = 0.

k_0 = 0.

H_0 = 0.


class H_Calculator(object):
    params = None

    def __init__(self, params):
        super().__init__()
        self.params = params


def H_z(n, r, t):
    return sum(
        f_a(i, n, t) * (r ** i)
        for i in (0, 1, 2)
    )


def f_a(i, n, t):
    return (k_0 * H_0 / 2.) * (
        cmath.exp(-t * (beta[1] - omega * 1j)) * B(i, 1, n) +
        cmath.exp(-t * (beta[2] - omega * 1j)) * B(i, 2, n) +
        cmath.exp(-t * (beta[1] + omega * 1j)) * B(i, 3, n) +
        cmath.exp(-t * (beta[2] + omega * 1j)) * B(i, 4, n) +
        cmath.exp(t * p(1)) * B(i, 5, n) +
        cmath.exp(t * p(2)) * B(i, 6, n)
    )


def B(i, j, n):
    if j == 1:

        return sum(
            (-C(i, k, n)) / (
                beta[1] - (omega * 1j) + p(k)
            )
            for k in (1, 2)
        ) + A(i, n)

    elif j == 2:
        return sum(
            C(i, k, n) / (
                beta[2] - (omega * 1j) + p(k)
            )
            for k in (1, 2)
        ) - A(i, n)

    elif j == 3:
        return sum(
            -C(i, k, n) / (
                beta[1] + (omega * 1j) + p(k)
            )
            for k in (1, 2)
        ) + A(i, n)

    elif j == 4:
        return sum(
            C(i, k, n) / (
                beta[2] + (omega * 1j) + p(k)
            )
            for k in (1, 2)
        ) - A(i, n)

    elif j == 5:
        return C(i, 1, n) * (
            1. / (beta[1] - omega * 1j + p(1)) -
            1. / (beta[2] - omega * 1j + p(1)) +
            1. / (beta[1] + omega * 1j + p(1)) -
            1. / (beta[2] + omega * 1j + p(1))
        )

    elif j == 6:
        return C(i, 2, n) * (
            1. / (beta[1] - omega * 1j + p(2)) -
            1. / (beta[2] - omega * 1j + p(2)) +
            1. / (beta[1] + omega * 1j + p(2)) -
            1. / (beta[2] + omega * 1j + p(2))
        )

    return 1.


def C(i, k, n):
    return (a(i, 1, n) * (A11(k) + A12(k)) +
            a(i, 2, n) * (A21(k) + A22(k)))


def A(i, n):
    return a(i, 3, n) + a(i, 4, n)


def A11(k):
    top = (p(k) - d(6)) * d(3) + d(2)*d(7)
    bottom = 2*p(k) - (d(1) + d(6))
    return top / bottom


def A12(k):
    top = (p(k) - d(6)) * d(4) + d(2)*d(8)
    bottom = 2 * p(k) - (d(1) + d(6))
    return top / bottom


def A21(k):
    top = (p(k) - d(1)) * d(7) + d(3)*d(5)
    bottom = 2*p(k) - d(1) + d(6)
    return top / bottom


def A22(k):
    top = (p(k) - d(1)) * d(8) + d(4)*d(5)
    bottom = 2*p(k) - (d(1) + d(6))
    return top / bottom


def p(k):
    assert k in (1, 2)
    # todo: implement
    return 1.

def alpha(i, n):
    # todo: implement
    return 1.


def d(j):
    # todo: implement
    if j in range(1, 4):
        return 0.
    elif j in range(4, 8):
        return 0
    else:
        raise CalculationError("Failed to calculate d({0})".format(j))


def a(i, j, n):
    # todo: implement
    return 0