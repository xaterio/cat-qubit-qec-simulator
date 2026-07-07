# Cat Qubit QEC Simulator

A comprehensive Python simulation of Schrodinger cat states in harmonic oscillators, modeling their uniquely biased noise profile and implementing quantum error correction for phase-flip errors. This project serves as a technical proof-of-concept for bosonic quantum computing architectures similar to Alice & Bob's approach.

## Physics Background

### Cat Qubits

Cat qubits encode quantum information in the superposition of coherent states in a harmonic oscillator. The logical basis states are defined as:

* **Logical $|0\rangle$ (Even cat state):**
  $$|0_L\rangle = \frac{|\alpha\rangle + |-\alpha\rangle}{\sqrt{2 + 2e^{-2|\alpha|^2}}}$$

* **Logical $|1\rangle$ (Odd cat state):**
  $$|1_L\rangle = \frac{|\alpha\rangle - |-\alpha\rangle}{\sqrt{2 - 2e^{-2|\alpha|^2}}}$$

where |alpha> is a coherent state with amplitude alpha. These states are macroscopic superpositions that exhibit quantum interference fringes in phase space.

### Wigner Functions

The Wigner function provides a quasi-probability distribution in phase space, allowing visualization of quantum states. For cat states, the Wigner function shows:
- Two positive lobes corresponding to the coherent states |alpha> and |-alpha>
- Quantum interference fringes at the origin (negative values), a signature of quantum superposition

### Biased Noise

Cat qubits exhibit a naturally biased noise channel due to the energy gap between even and odd parity states:
- Bit-flip errors: Suppressed exponentially with |alpha|^2
- Phase-flip errors: Scale linearly with |alpha|^2

This bias enables hardware-efficient quantum error correction, as only phase-flips need active correction.

### Quantum Error Correction

The repetition code corrects phase-flip errors by encoding a logical qubit across multiple physical cat qubits. The stabilizers are Z_i Z_{i+1} measurements, which detect phase-flip errors without collapsing the superposition.

## Installation

### Requirements

- Python 3.10+
- QuTiP 5.0+
- NumPy 1.24+
- Matplotlib 3.7+
- Pytest 7.4+

### Setup

1. Clone the repository:
```bash
git clone https://github.com/xaterio/cat-qubit-qec-simulator.git
cd cat-qubit-qec-simulator
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
cat-qubit-qec-simulator/
├── src/
│   ├── __init__.py
│   ├── cat_state.py       # Cat state generation
│   ├── visualization.py   # Wigner function plotting
│   ├── noise_model.py     # Noise simulation
│   └── qec.py            # Quantum error correction
├── tests/
│   ├── test_cat_state.py
│   ├── test_visualization.py
│   ├── test_noise_model.py
│   └── test_qec.py
├── results/              # Generated plots and data
├── docs/                # Additional documentation
├── requirements.txt
└── README.md
```

## Usage

### Running Tests

Execute the test suite to verify the implementation:

```bash
pytest tests/
```

For verbose output:
```bash
pytest tests/ -v
```

### Example: Cat State Generation

```python
from src.cat_state import CatState

# Create a cat state with alpha=2.0 in a 30-dimensional Fock space
cat = CatState(n_cavity=30, alpha=2.0)

# Generate logical states
logical_zero = cat.logical_zero()  # Even cat state
logical_one = cat.logical_one()    # Odd cat state

# Compute average photon number
avg_photons = cat.photon_number_expectation(logical_zero)
print(f"Average photon number: {avg_photons}")
```

### Example: Wigner Function Visualization

```python
from src.cat_state import CatState
from src.visualization import plot_wigner_function

cat = CatState(n_cavity=30, alpha=2.0)
even_cat = cat.even_cat_state()

# Plot and save Wigner function
plot_wigner_function(
    even_cat,
    title='Even Cat State (alpha=2.0)',
    save_path='results/wigner_even.png'
)
```

### Example: Biased Noise Analysis

```python
import numpy as np
from src.noise_model import compute_bit_flip_rate, compute_phase_flip_rate, plot_biased_noise
from src.cat_state import CatState

# Analyze noise across different alpha values
alpha_range = np.linspace(1.0, 3.0, 20)
bit_flip_rates = compute_bit_flip_rate(CatState, alpha_range)
phase_flip_rates = compute_phase_flip_rate(CatState, alpha_range)

# Plot the biased noise profile
plot_biased_noise(
    alpha_range,
    bit_flip_rates,
    phase_flip_rates,
    save_path='results/biased_noise.png'
)
```

### Example: Quantum Error Correction

```python
from src.qec import RepetitionCode

# Create a 3-qubit repetition code
code = RepetitionCode(n_qubits=3, n_cavity=30, alpha=2.0)

# Encode logical zero
logical_zero = code.encode_logical_zero()

# Simulate a phase-flip error on the first qubit
error_pattern = [1, 0, 0]
corrupted_state, recovered_state, syndrome, correction = code.simulate_error_correction(
    logical_zero, error_pattern
)

# Check recovery fidelity
fidelity = code.logical_fidelity(logical_zero, recovered_state)
print(f"Recovery fidelity: {fidelity}")
```

### Example: Complete Simulation Workflow

```python
import numpy as np
from src.cat_state import CatState
from src.visualization import plot_wigner_function, plot_cat_state_comparison
from src.noise_model import plot_biased_noise, simulate_noise_dynamics
from src.qec import simulate_qec_performance

# 1. Generate and visualize cat states
cat = CatState(n_cavity=30, alpha=2.0)
plot_cat_state_comparison(cat, [1.5, 2.0, 2.5], save_dir='results')

# 2. Analyze biased noise
alpha_range = np.linspace(1.0, 3.0, 20)
bit_flip_rates = compute_bit_flip_rate(CatState, alpha_range)
phase_flip_rates = compute_phase_flip_rate(CatState, alpha_range)
plot_biased_noise(alpha_range, bit_flip_rates, phase_flip_rates, 
                 save_path='results/biased_noise.png')

# 3. Simulate noise dynamics
simulate_noise_dynamics(cat, alpha=2.0, save_path='results/noise_dynamics.png')

# 4. Evaluate QEC performance
n_qubits_list = [3, 5, 7]
alpha_values = [1.5, 2.0, 2.5]
results = simulate_qec_performance(n_qubits_list, alpha_values)
```

## Key Features

### Cat State Generation
- Even and odd Schrodinger cat states
- Logical qubit encoding
- Photon number expectation
- Parity operator
- Displacement operators

### Phase Space Visualization
- 2D Wigner function contour plots
- 3D Wigner function surface plots
- Batch generation for multiple alpha values
- High-resolution output for publications

### Noise Modeling
- Lindblad master equation solver
- Single-photon loss channel
- Bit-flip rate computation (exponential suppression)
- Phase-flip rate computation (linear scaling)
- Time evolution under noise

### Quantum Error Correction
- Phase-flip repetition code
- Stabilizer generator construction
- Syndrome measurement
- Error correction and recovery
- Logical fidelity computation
- Performance benchmarking

## Theoretical Details

### Bit-Flip Suppression

The bit-flip rate for cat qubits scales as:
```
Gamma_X ~ kappa * exp(-2|alpha|^2)
```

where kappa is the photon loss rate. This exponential suppression arises from the energy gap between even and odd parity states.

### Phase-Flip Rate

The phase-flip rate scales linearly with the average photon number:
```
Gamma_Z ~ kappa * |alpha|^2
```

This linear scaling reflects the increased sensitivity to photon loss at higher energies.

### Repetition Code Threshold

The repetition code can correct up to floor((n-1)/2) phase-flip errors, where n is the number of physical qubits. The biased noise of cat qubits makes this approach particularly efficient.

## Performance Considerations

- Fock space truncation: Default n_cavity=30 provides good accuracy for alpha up to ~3.0
- Simulation time: Scales exponentially with the number of qubits in the repetition code
- Memory usage: Large Hilbert spaces may require significant RAM for multi-qubit simulations

## Contributing

Contributions are welcome. Please ensure:
- Code follows PEP-8 style guidelines
- All tests pass before submitting
- New features include corresponding tests
- Documentation is updated for any API changes

## License

This project is provided as-is for educational and research purposes.

## References

1. Mirrahimi, M., et al. "Dynamically protected cat-qubits: a new paradigm for universal quantum computation." New Journal of Physics 16.4 (2014): 045014.
2. Ofek, N., et al. "Extending the lifetime of a quantum bit with error correction in superconducting circuits." Nature 536.7616 (2016): 441-445.
3. Leghtas, Z., et al. "Hardware-efficient autonomous quantum memory protection against photon loss." Physical Review A 88.2 (2013): 023849.
