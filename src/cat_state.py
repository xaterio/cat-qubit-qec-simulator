import numpy as np
from qutip import coherent, basis, destroy, fock_dm, Qobj


class CatState:
    def __init__(self, n_cavity, alpha):
        self.n_cavity = n_cavity
        self.alpha = alpha
        self.a = destroy(n_cavity)
        self.coherent_plus = coherent(n_cavity, alpha)
        self.coherent_minus = coherent(n_cavity, -alpha)

    def even_cat_state(self):
        norm = np.sqrt(2 + 2 * np.exp(-2 * np.abs(self.alpha)**2))
        cat = (self.coherent_plus + self.coherent_minus) / norm
        return cat

    def odd_cat_state(self):
        norm = np.sqrt(2 - 2 * np.exp(-2 * np.abs(self.alpha)**2))
        cat = (self.coherent_plus - self.coherent_minus) / norm
        return cat

    def logical_zero(self):
        return self.even_cat_state()

    def logical_one(self):
        return self.odd_cat_state()

    def photon_number_expectation(self, state):
        n_op = self.a.dag() * self.a
        return (n_op * state).tr()

    def displacement_operator(self, beta):
        from qutip import displace
        return displace(self.n_cavity, beta)

    def parity_operator(self):
        parity = Qobj(np.zeros((self.n_cavity, self.n_cavity)))
        for n in range(self.n_cavity):
            parity += ((-1)**n) * fock_dm(self.n_cavity, n)
        return parity
