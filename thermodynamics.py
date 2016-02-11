# coding = utf-8

import cmath
import math
import decimal

from errors import CalculationError
import params
from matrix import Matrix


def solve_quadratic(a, b, c):
        D = b**2 - 4*a*c
        x1 = (-b - cmath.sqrt(D)) / (2*a)
        x2 = (-b + cmath.sqrt(D)) / (2*a)
        return x1, x2

class H_Calculator(object):
    parm = None
    prop = None

    mat_i = None
    mat_o = None

    mat_A = None

    _a = {}

    def __init__(self, calculation_parameters, material_inner, material_outer):
        """

        :param calculation_parameters:
        :type calculation_parameters: params.CalculationParameters
        :type material_inner: params.MaterialProperties
        :type material_outer: params.MaterialProperties
        :return:
        """
        super().__init__()
        self.parm = calculation_parameters
        self.mat_i = material_inner
        self.mat_o = material_outer
        self.build_A()

    def build_A(self):
        r = self.parm.r
        k = self.mat_i['sigma'] / self.mat_o['sigma']
        data = [
            [(r[1] ** 2 - r[0] ** 2) / 2., (r[1] ** 3 - r[0] ** 3) / 3., (r[1] ** 4 - r[0] ** 4) / 4.,
             (r[2] ** 2 - r[1] ** 2) / 2., (r[2] ** 3 - r[1] ** 3) / 3., (r[2] ** 4 - r[1] ** 4) / 4.],
            [(r[1] ** 3 - r[0] ** 3) / 3., (r[1] ** 4 - r[0] ** 4) / 4., (r[1] ** 5 - r[0] ** 5) / 5.,
             (r[2] ** 3 - r[1] ** 3) / 3., (r[2] ** 4 - r[1] ** 4) / 4., (r[2] ** 5 - r[1] ** 5) / 5.],
            [1., r[0], r[0] ** 2, 0, 0, 0],
            [0, 0, 0, 1, r[2], r[2] ** 2],
            [1, r[1], r[1] ** 2, -1, -r[1], -r[1] ** 2],
            [0, 1, 2 * r[1], 0, -k, -2 * k * r[1]],
        ]

        def fmt(x):
            return '{:e}'.format(x)

        for row in data:
            print('\t'.join(map(fmt, row)))
        self.mat_A = Matrix(data)
        print("Det(A) = " + fmt(self.mat_A._det))

    def a_ij(self, i, j):
        assert i in (0, 1, 2)
        assert j in (1, 2, 3, 4)

        return self.mat_A.item(j, i+1)

    def a(self, i, j, n):
        assert i in (0, 1, 2)
        assert j in (1, 2, 3, 4)
        assert n in (1, 2)

        if j in (1, 2):
            if n == 1:
                return self.mat_A.item(j, i+1)
            elif n == 2:
                return self.mat_A.item(j, i+4)
        elif j in (3, 4):
            if n == 1:
                return self.mat_A.item(j+2, i+1)
            elif n == 2:
                return self.mat_A.item(j+2, i+4)

    def H(self, r, t):
        n = lambda x: 1 if x < self.parm.r[1] else 2
        arr = [self.f_a(i, n(r), t) * (r ** i)
               for i in (0, 1, 2)]
        return sum(arr)

    def f_a(self, i, n, t):
        assert i in (0, 1, 2)
        assert n in (1, 2)
        return (self.parm.k_0 * self.parm.H_0 / 2.) * (
            cmath.exp(-t * (self.parm.beta_1 - self.parm.omega * 1j)) * self.B(i, 1, n) +
            cmath.exp(-t * (self.parm.beta_2 - self.parm.omega * 1j)) * self.B(i, 2, n) +
            cmath.exp(-t * (self.parm.beta_1 + self.parm.omega * 1j)) * self.B(i, 3, n) +
            cmath.exp(-t * (self.parm.beta_2 + self.parm.omega * 1j)) * self.B(i, 4, n) +
            cmath.exp(t * self.p(1)) * self.B(i, 5, n) +
            cmath.exp(t * self.p(2)) * self.B(i, 6, n)
        )

    def B(self, i, j, n):
        assert i in (0, 1, 2)
        assert j in (1, 2, 3, 4, 5, 6)
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
        assert i in (0, 1, 2)
        return (self.a(i, 1, n) * (self.A11(k) + self.A12(k)) +
                self.a(i, 2, n) * (self.A21(k) + self.A22(k)))

    def A(self, i, n):
        assert i in (0, 1, 2)
        return self.a(i, 3, n) + self.a(i, 4, n)

    def A11(self, k):
        assert k in (1, 2)
        top = (self.p(k) - self.d(6)) * self.d(3) + self.d(2)*self.d(7)
        bottom = 2*self.p(k) - (self.d(1) + self.d(6))
        return top / bottom

    def A12(self, k):
        assert k in (1, 2)
        top = (self.p(k) - self.d(6)) * self.d(4) + self.d(2)*self.d(8)
        bottom = 2 * self.p(k) - (self.d(1) + self.d(6))
        return top / bottom

    def A21(self, k):
        assert k in (1, 2)
        top = (self.p(k) - self.d(1)) * self.d(7) + self.d(3)*self.d(5)
        bottom = 2*self.p(k) - self.d(1) + self.d(6)
        return top / bottom

    def A22(self, k):
        assert k in (1, 2)
        top = (self.p(k) - self.d(1)) * self.d(8) + self.d(4)*self.d(5)
        bottom = 2*self.p(k) - (self.d(1) + self.d(6))
        return top / bottom

    def p(self, k):
        assert k in (1, 2)

        a = 1
        b = -(self.d(1) + self.d(6))
        c = self.d(1) * self.d(6) - self.d(2) * self.d(5)

        # print("Quadratic equation: ")
        # print('a, b, c == {a:e}, {b:e}, {c:e}'.format(a=a, b=b, c=c))

        p1, p2 = solve_quadratic(1,
                                 -(self.d(1) + self.d(6)),
                                 self.d(1) * self.d(6) - self.d(2) * self.d(5))
        if k == 1:
            return p1
        elif k == 2:
            return p2

    def alpha(self, i, n):
        return (self.parm.r[n]**i - self.parm.r[n-1]**i) / float(i)

    def d(self, j):
        arr = [-14964970.1695227,
               1569092065.69423,
               14.9639589435456,
               -0.833471911731994,
               -124977.635865608,
               13086357.116585,
               0.126968410318618,
               -0.00608505570217171]
        return arr[j-1]

        sigma = (0, self.mat_i['sigma'], self.mat_o['sigma'])
        mu = (0, self.mat_i['mu'], self.mat_o['mu'])
        if j in (1, 2, 3, 4):
            return sum((
                (self.a(1, j, n) * self.alpha(1, n) + 4*self.a(2, j, n) * self.alpha(2, n)) /
                (sigma[n] * mu[n])
                for n in (1, 2)
            ))
        elif j in (5, 6, 7, 8):
            j = j % 4 + 1
            return sum((
                (self.a(1, j, n) * self.alpha(2, n) + 4*self.a(2, j, n) * self.alpha(3, n)) /
                (sigma[n] * mu[n])
                for n in (1, 2)
            ))
        else:
            raise CalculationError("Failed to calculate d({0})".format(j))


class QF_Calculator(object):
    h = None
    parm = None
    prop = None

    alphas = None
    Cs = None

    def __init__(self, h_calculator, properties):
        """

        :param h_calculator:
        :type h_calculator: H_Calculator
        :return:
        """
        self.h = h_calculator
        self.parm = self.h.parm
        self.prop = properties

        self.alphas= {
            1: -2 * (self.parm.beta_1 - self.parm.omega * 1j),
            2: -1 * (self.parm.beta_1 + self.parm.beta_2 - 2j*self.parm.omega),
            3: -2 * self.parm.beta_1,
            4: -1 * (self.parm.beta_1 + self.parm.beta_2),
            5: -1 * (self.parm.beta_1 - 1j*self.parm.omega - self.h.p(1)),
            6: -1 * (self.parm.beta_1 - 1j*self.parm.omega - self.h.p(2)),
            7: -2 * (self.parm.beta_2 - 1j*self.parm.omega),
            8: -2 * self.parm.beta_2,
            9: -1 * (self.parm.beta_2 - 1j*self.parm.omega),
            10: -1 * (self.parm.beta_2 - 1j*self.parm.omega - self.h.p(2)),
            11: -2 * (self.parm.beta_1 + 1j*self.parm.omega),
            12: -1 * (self.parm.beta_1 + self.parm.beta_2 + 2j*self.parm.omega),
            13: -1 * (self.parm.beta_1 + 1j*self.parm.omega - self.h.p(1)),
            14: -1 * (self.parm.beta_1 + 1j*self.parm.omega - self.h.p(2)),
            15: -1 * (self.parm.beta_2 + 1j*self.parm.omega),
            16: -1 * (self.parm.beta_2 + 1j*self.parm.omega - self.h.p(1)),
            17: -1 * (self.parm.beta_2 + 1j*self.parm.omega - self.h.p(2)),
            18: 2 * self.h.p(1),
            19: self.h.p(1) + self.h.p(2),
            20: 2 * self.h.p(2),
        }

    def Q(self, r, t):
        n = lambda x: 1 if r < self.parm.r[1] else 2
        q = self.parm.k_0**2 * self.parm.H_0**2 / (self.prop[n(r)].sigma * 4)
        q *= sum((
            i*j*self.C(l, i, j, n(r)) * cmath.exp(self.alpha(l)*t) * math.pow(r, i+j-2)

            for i in (1, 2)
            for j in (1, 2)
            for l in range(1, 21)
        ))

        return 1

    def F(self, r, t):
        n = lambda x: 1 if r < self.parm.r[1] else 2
        f = - self.prop[n(r)].mu * self.parm.k_0**2 * self.parm.H_0**2 / 4
        f *= sum((
            i * self.C(l, i, j, n(r)) * cmath.exp(self.alpha(l) * t) * math.pow(r, i+j-1)

            for i in (1, 2)
            for j in (1, 2)
            for l in range(1, 21)
        ))
        return f

    def alpha(self, i):
        assert i in range(1, 21)
        return self.alphas[i]

    def C(self, l, i, j, n):
        B = lambda _i, _j: self.h.B(_i, _j, n)

        if l == 1:
            return B(i, 1) * B(j, 1)
        elif l == 2:
            return B(i, 1) * B(j, 2) + B(i, 2) * B(j, 1)
        elif l == 3:
            return B(i, 1) * B(j, 3) + B(i, 3) * B(j, 1)
        elif l == 4:
            return B(i, 1) * B(j, 4) + B(i, 4) * B(j, 1) + B(i, 2) * B(j, 3) + B(i, 3) * B(j, 2)
        elif l == 5:
            return B(i, 1) * B(j, 5) + B(i, 5) * B(j, 1)
        elif l == 6:
            return B(i, 1) * B(j, 6) + B(i, 6) * B(j, 1)
        elif l == 7:
            return B(i, 2) * B(j, 2)
        elif l == 8:
            return B(i, 2) * B(j, 4) + B(i, 4) * B(j, 2)
        elif l == 9:
            return B(i, 2) * B(j, 5) + B(i, 5) * B(j, 2)
        elif l == 10:
            return B(i, 2) * B(j, 6) + B(i, 6) * B(j, 2)
        elif l == 11:
            return B(i, 3) * B(j, 3)
        elif l == 12:
            return B(i, 3) * B(j, 4) + B(i, 4) * B(j, 3)
        elif l == 13:
            return B(i, 3) * B(j, 5) + B(i, 5) * B(j, 3)
        elif l == 14:
            return B(i, 3) * B(j, 6) + B(i, 6) * B(j, 3)
        elif l == 15:
            return B(i, 4) * B(j, 4)
        elif l == 16:
            return B(i, 4) * B(j, 5) + B(i, 5) * B(j, 4)
        elif l == 17:
            return B(i, 4) * B(j, 6) + B(i, 6) * B(j, 4)
        elif l == 18:
            return B(i, 5) * B(j, 5)
        elif l == 19:
            return B(i, 5) * B(j, 6) + B(i, 6) * B(j, 5)
        elif l == 20:
            return B(i, 6) * B(j, 6)


class T_Calculator(object):
    parm = None
    prop = None
    qf = None

    def __init__(self, qf_calculator, parameters, properties):
        """
        :type parameters: params.CalculationParameters
        :param qf_calculator:
        :type qf_calculator: QF_Calculator
        :param properties:
        :return:
        """

        self.qf = qf_calculator
        self.parm = parameters
        self.prop = properties

    def T(self, r, t, n):
        return sum((
            self.b_f(t, p, n) * math.pow(r, p)

            for p in (0, 1, 2)
        ))

    def b_f(self, t, p, n):
        b = self.parm.k_0**2 * self.parm.H_0**2 / 4
        b *= sum((
            i*j*self.M(i, j, l, m, n) *
            (cmath.exp(self.p(m)*t) - cmath.exp(self.qf.alpha(l)*t))
                / (self.p(m) - self.qf.alpha(l))

            for m in (1, 2)
            for i in (1, 2)
            for j in (1, 2)
            for l in range(1, 21)
        ))
        return b

    def M(self, i, j, l, m, n):
        # todo: check
        m_1 = self.b(self.p(1), 1, n) * (self.N(1, i, j, l) * self.B(1, 1, m) + self.N(2, i, j, l) * self.B(1, 2, m))
        m_2 = self.b(self.p(2), 2, n) * (self.N(1, i, j, l) * self.B(2, 1, m) + self.N(2, i, j, l) * self.B(2, 2, m))
        return m_1 + m_2

    def N(self, k, i, j, l):
        if k == 1:
            n1 = ((self.prop[0].k + (self.parm.r[1] ** (i + j) - self.parm.r[0] ** (i + j))) * self.qf.C(i, j, l, 1) /
                    (self.prop[0].sigma * self.prop[0]['lambda'] * (i + j)))
            n2 = ((self.prop[1].k + (self.parm.r[2] ** (i + j) - self.parm.r[1] ** (i + j))) * self.qf.C(i, j, l, 2) /
                    (self.prop[1].sigma * self.prop[1]['lambda'] * (i + j)))
            return n1 + n2
        elif k == 2:
            n1 = ((self.prop[0].k + (self.parm.r[1] ** (i + j + 1) - self.parm.r[0] ** (i + j + 1))) * self.qf.C(i, j, l, 1) /
                    (self.prop[0].sigma * self.prop[0]['lambda'] * (i + j + 1)))
            n2 = ((self.prop[1].k + (self.parm.r[2] ** (i + j + 1) - self.parm.r[1] ** (i + j + 1))) * self.qf.C(i, j, l, 2) /
                    (self.prop[1].sigma * self.prop[1]['lambda'] * (i + j + 1)))
            return n1 + n2
        raise Exception("N calculation failure")

    def B(self, i, j, m):
        if (i, j) == (1, 1):
            return (self.p(m) - self.d(4)) / (2*self.p(m) - (self.d(1) + self.d(4)))
        elif (i, j) == (1, 2):
            return self.d(2) / (2*self.p(m) - (self.d(1) + self.d(4)))
        elif (i, j) == (2, 1):
            return self.d(3) / (2*self.p(m) - (self.d(1) + self.d(4)))
        elif (i, j) == (2, 2):
            return (self.p(m) - self.d(1)) / (2*self.p(m) - (self.d(1) + self.d(4)))
        return 0

    def b(self, i, j, n):
        # todo: implement
        return 0

    def p(self, m):
        return 0

    def d(self, j):
        assert (j in range(1, 5))
        return 0