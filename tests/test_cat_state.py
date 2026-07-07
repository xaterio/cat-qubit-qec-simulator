import pytest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from cat_state import CatState
from qutip import fock_dm


def test_cat_state_initialization():
    n_cavity = 30
    alpha = 2.0
    cat = CatState(n_cavity, alpha)
    
    assert cat.n_cavity == n_cavity
    assert cat.alpha == alpha


def test_even_cat_state_normalization():
    n_cavity = 30
    alpha = 2.0
    cat = CatState(n_cavity, alpha)
    even_cat = cat.even_cat_state()
    
    norm = np.sqrt((even_cat.dag() * even_cat).tr())
    assert np.abs(norm - 1.0) < 1e-10


def test_odd_cat_state_normalization():
    n_cavity = 30
    alpha = 2.0
    cat = CatState(n_cavity, alpha)
    odd_cat = cat.odd_cat_state()
    
    norm = np.sqrt((odd_cat.dag() * odd_cat).tr())
    assert np.abs(norm - 1.0) < 1e-10


def test_logical_states_orthogonality():
    n_cavity = 30
    alpha = 2.0
    cat = CatState(n_cavity, alpha)
    
    logical_zero = cat.logical_zero()
    logical_one = cat.logical_one()
    
    overlap = abs((logical_zero.dag() * logical_one).tr())
    assert overlap < 1e-10


def test_photon_number_expectation():
    n_cavity = 30
    alpha = 2.0
    cat = CatState(n_cavity, alpha)
    even_cat = cat.even_cat_state()
    
    avg_photons = cat.photon_number_expectation(even_cat)
    expected = alpha**2
    
    assert np.abs(avg_photons - expected) < 0.5


def test_parity_operator():
    n_cavity = 30
    alpha = 2.0
    cat = CatState(n_cavity, alpha)
    
    parity = cat.parity_operator()
    even_cat = cat.even_cat_state()
    odd_cat = cat.odd_cat_state()
    
    even_parity = (even_cat.dag() * parity * even_cat).tr()
    odd_parity = (odd_cat.dag() * parity * odd_cat).tr()
    
    assert even_parity.real > 0
    assert odd_parity.real < 0
