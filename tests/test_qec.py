import pytest
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from qec import RepetitionCode


def test_repetition_code_initialization():
    n_qubits = 3
    n_cavity = 30
    alpha = 2.0
    code = RepetitionCode(n_qubits, n_cavity, alpha)
    
    assert code.n_qubits == n_qubits
    assert code.n_cavity == n_cavity
    assert code.alpha == alpha


def test_logical_zero_encoding():
    n_qubits = 3
    n_cavity = 30
    alpha = 2.0
    code = RepetitionCode(n_qubits, n_cavity, alpha)
    
    logical_zero = code.encode_logical_zero()
    
    assert logical_zero.shape == (n_cavity**n_qubits, n_cavity**n_qubits)


def test_logical_one_encoding():
    n_qubits = 3
    n_cavity = 30
    alpha = 2.0
    code = RepetitionCode(n_qubits, n_cavity, alpha)
    
    logical_one = code.encode_logical_one()
    
    assert logical_one.shape == (n_cavity**n_qubits, n_cavity**n_qubits)


def test_stabilizer_generators():
    n_qubits = 3
    n_cavity = 30
    alpha = 2.0
    code = RepetitionCode(n_qubits, n_cavity, alpha)
    
    stabilizers = code.stabilizer_generators()
    
    assert len(stabilizers) == n_qubits - 1


def test_syndrome_measurement():
    n_qubits = 3
    n_cavity = 30
    alpha = 2.0
    code = RepetitionCode(n_qubits, n_cavity, alpha)
    
    logical_zero = code.encode_logical_zero()
    syndrome = code.measure_syndrome(logical_zero)
    
    assert len(syndrome) == n_qubits - 1
    assert all(s == 1 for s in syndrome)


def test_phase_flip_application():
    n_qubits = 3
    n_cavity = 30
    alpha = 2.0
    code = RepetitionCode(n_qubits, n_cavity, alpha)
    
    logical_zero = code.encode_logical_zero()
    flipped_state = code.apply_phase_flip(logical_zero, 0)
    
    assert flipped_state.shape == logical_zero.shape


def test_error_correction():
    n_qubits = 3
    n_cavity = 30
    alpha = 2.0
    code = RepetitionCode(n_qubits, n_cavity, alpha)
    
    logical_zero = code.encode_logical_zero()
    error_pattern = [1, 0, 0]
    
    corrupted_state, recovered_state, syndrome, correction = code.simulate_error_correction(
        logical_zero, error_pattern
    )
    
    assert len(syndrome) == n_qubits - 1
    assert len(correction) == n_qubits


def test_logical_fidelity():
    n_qubits = 3
    n_cavity = 30
    alpha = 2.0
    code = RepetitionCode(n_qubits, n_cavity, alpha)
    
    logical_zero = code.encode_logical_zero()
    fidelity = code.logical_fidelity(logical_zero, logical_zero)
    
    assert np.abs(fidelity - 1.0) < 1e-10
