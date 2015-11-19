# coding = utf-8


class MaterialProperties(object):
    STEEL = 'steel'
    COPPER = 'copper'
    ALUMINIUM = 'aluminium'

    material_type = None
    data = {
        STEEL: {
            'sigma': 0.135 * (10 ** 7),
            'mu': 12.57 * (10 ** -7),
            'nu': 0.283,
            'k': 0.422 * (10 ** -5),
            'lambda': 0.167 * (10 ** 2),
            'E': 0.192 * (10 ** 12),
            'alpha': 0.17 * (10 ** -4),
            'rho': 7850,
            'sigma_t': 300,
        },
        COPPER: {
            'sigma': 0.588 * (10 ** 8),
            'mu': 12.57 * (10 ** -7),
            'nu': 0.35,
            'k': 0.118 * (10 ** -3),
            'lambda': 0.406 * (10 ** 3),
            'E': 0.129 * (10 ** 12),
            'alpha': 0.178 * (10 ** -4),
            'rho': 8900,
            'sigma_t': 70,
        },
        ALUMINIUM: {
            'sigma': 0.363 * (10 ** 8),
            'mu': 12.57 * (10 ** -7),
            'nu': 0.34,
            'k': 0.847 * (10 ** -4),
            'lambda': 0.209 * (10 ** 3),
            'E': 0.71 * (10 ** 11),
            'alpha': 0.229 * (10 ** -4),
            'rho': 2670,
            'sigma_t': 30,
        },
    }

    def __init__(self, material_type):
        self.material_type = material_type

    def __getitem__(self, item):
        return self.data[self.material_type][item]


class CalculationParameters(object):
    H_0 = 1
    t_i = None
    r = (0.008, 0.009, 0.01)
    beta_1 = None
    beta_2 = None
    k_0 = 4

    def __init__(self, t_i):
        self.t_i = t_i
        self.beta_1 = 6.9 / t_i
        self.beta_2 = 2 * self.beta_1

