import pytest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from visualization import plot_wigner_function
from cat_state import CatState


def test_wigner_function_shape():
    n_cavity = 30
    alpha = 2.0
    cat = CatState(n_cavity, alpha)
    even_cat = cat.even_cat_state()
    
    W = plot_wigner_function(even_cat, save_path=None)
    
    assert W.shape == (100, 100)


def test_wigner_function_range():
    n_cavity = 30
    alpha = 2.0
    cat = CatState(n_cavity, alpha)
    even_cat = cat.even_cat_state()
    
    W = plot_wigner_function(even_cat, save_path=None)
    
    assert W.min() >= -0.5
    assert W.max() <= 0.5


def test_wigner_function_interference():
    n_cavity = 30
    alpha = 2.0
    cat = CatState(n_cavity, alpha)
    even_cat = cat.even_cat_state()
    
    W = plot_wigner_function(even_cat, save_path=None)
    
    center_idx = W.shape[0] // 2
    center_value = W[center_idx, center_idx]
    
    assert center_value < 0
