import pytest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from noise_model import NoiseModel, compute_bit_flip_rate, compute_phase_flip_rate
from cat_state import CatState


def test_noise_model_initialization():
    n_cavity = 30
    kappa = 0.1
    noise = NoiseModel(n_cavity, kappa)
    
    assert noise.n_cavity == n_cavity
    assert noise.kappa == kappa


def test_bit_flip_rate_exponential_decay():
    alpha_range = np.linspace(1.0, 3.0, 5)
    bit_flip_rates = compute_bit_flip_rate(CatState, alpha_range)
    
    assert len(bit_flip_rates) == len(alpha_range)
    assert all(bit_flip_rates[i] > bit_flip_rates[i+1] 
               for i in range(len(bit_flip_rates)-1))


def test_phase_flip_rate_linear_growth():
    alpha_range = np.linspace(1.0, 3.0, 5)
    phase_flip_rates = compute_phase_flip_rate(CatState, alpha_range)
    
    assert len(phase_flip_rates) == len(alpha_range)
    assert all(phase_flip_rates[i] < phase_flip_rates[i+1] 
               for i in range(len(phase_flip_rates)-1))


def test_noise_evolution():
    n_cavity = 30
    kappa = 0.1
    noise = NoiseModel(n_cavity, kappa)
    
    cat = CatState(n_cavity, 2.0)
    initial_state = cat.logical_zero()
    
    tlist = np.linspace(0, 1, 10)
    states = noise.evolve_state(initial_state, tlist)
    
    assert len(states) == len(tlist)
