# coding = utf-8

import cmath

from errors import CalculationError
from params import MaterialProperties


class H_Calculator(object):
    parm = None
    prop = None

    def __init__(self, calculation_parameters, material_properties):
        super().__init__()
        self.parm = calculation_parameters
        self.prop = material_properties

    def H(self, n, r, t):
        return sum(
            self.f_a(i, n, t) * (r ** i)
            for i in (0, 1, 2)
        )

    def f_a(self, i, n, t):
        return (self.parm.k_0 * self.parm.H_0 / 2.) * (
            cmath.exp(-t * (self.parm.beta_1 - self.parm.omega * 1j)) * self.B(i, 1, n) +
            cmath.exp(-t * (self.parm.beta_2 - self.parm.omega * 1j)) * self.B(i, 2, n) +
            cmath.exp(-t * (self.parm.beta_1 + self.parm.omega * 1j)) * self.B(i, 3, n) +
            cmath.exp(-t * (self.parm.beta_2 + self.parm.omega * 1j)) * self.B(i, 4, n) +
            cmath.exp(t * self.p(1)) * self.B(i, 5, n) +
            cmath.exp(t * self.p(2)) * self.B(i, 6, n)
        )

    def B(self, i, j, n):
        if j == 1:

            return sum(
                (-self.C(i, k, n)) / (
                    self.parm.beta_1 - (self.parm.omega * 1j) + self.p(k)
                )
                for k in (1, 2)
            ) + self.A(i, n)

        elif j == 2:
            return sum(
                self.C(i, k, n) / (
                    self.parm.beta_2 - (self.parm.omega * 1j) + self.p(k)
                )
                for k in (1, 2)
            ) - self.A(i, n)

        elif j == 3:
            return sum(
                -self.C(i, k, n) / (
                    self.parm.beta_1 + (self.parm.omega * 1j) + self.p(k)
                )
                for k in (1, 2)
            ) + self.A(i, n)

        elif j == 4:
            return sum(
                self.C(i, k, n) / (
                    self.parm.beta_2 + (self.parm.omega * 1j) + self.p(k)
                )
                for k in (1, 2)
            ) - self.A(i, n)

        elif j == 5:
            return self.C(i, 1, n) * (
                1. / (self.parm.beta_1 - self.parm.omega * 1j + self.p(1)) -
                1. / (self.parm.beta_2 - self.parm.omega * 1j + self.p(1)) +
                1. / (self.parm.beta_1 + self.parm.omega * 1j + self.p(1)) -
                1. / (self.parm.beta_2 + self.parm.omega * 1j + self.p(1))
            )

        elif j == 6:
            return self.C(i, 2, n) * (
                1. / (self.parm.beta_1 - self.parm.omega * 1j + self.p(2)) -
                1. / (self.parm.beta_2 - self.parm.omega * 1j + self.p(2)) +
                1. / (self.parm.beta_1 + self.parm.omega * 1j + self.p(2)) -
                1. / (self.parm.beta_2 + self.parm.omega * 1j + self.p(2))
            )

        assert False

    def C(self, i, k, n):
        return (self.a(i, 1, n) * (self.A11(k) + self.A12(k)) +
                self.a(i, 2, n) * (self.A21(k) + self.A22(k)))

    def A(self, i, n):
        return self.a(i, 3, n) + self.a(i, 4, n)

    def A11(self, k):
        top = (self.p(k) - self.d(6)) * self.d(3) + self.d(2)*self.d(7)
        bottom = 2*self.p(k) - (self.d(1) + self.d(6))
        return top / bottom

    def A12(self, k):
        top = (self.p(k) - self.d(6)) * self.d(4) + self.d(2)*self.d(8)
        bottom = 2 * self.p(k) - (self.d(1) + self.d(6))
        return top / bottom

    def A21(self, k):
        top = (self.p(k) - self.d(1)) * self.d(7) + self.d(3)*self.d(5)
        bottom = 2*self.p(k) - self.d(1) + self.d(6)
        return top / bottom

    def A22(self, k):
        top = (self.p(k) - self.d(1)) * self.d(8) + self.d(4)*self.d(5)
        bottom = 2*self.p(k) - (self.d(1) + self.d(6))
        return top / bottom

    def p(self, k):
        assert k in (1, 2)

        p1, p2 = self.solve_quadratic(1,
                                      -(self.d(1) + self.d(6)),
                                      self.d(1) * self.d(6) - self.d(2) * self.d(5))
        if k == 1:
            return p1
        elif k == 2:
            return p2

    def solve_quadratic(self, a, b, c):
        D = b**2 - 4*a*c
        x1 = (-b - cmath.sqrt(D)) / (2*a)
        x2 = (-b + cmath.sqrt(D)) / (2*a)
        return x1, x2

    def alpha(self, i, n):
        # todo: implement
        return 1.

    def d(self, j):
        # todo: implement
        if j in range(1, 5):
            return 0.
        elif j in range(5, 9):
            return 1.
        else:
            raise CalculationError("Failed to calculate d({0})".format(j))

    def a(self, i, j, n):
        # todo: implement
        return 1.
