import numpy as np
import matplotlib.pyplot as plt
from qutip import mesolve, destroy, fock_dm, basis, Qobj
import os
from .cat_state import CatState


class NoiseModel:
    def __init__(self, n_cavity, kappa):
        self.n_cavity = n_cavity
        self.kappa = kappa
        self.a = destroy(n_cavity)
        
    def photon_loss_lindblad(self):
        return np.sqrt(self.kappa) * self.a
    
    def evolve_state(self, initial_state, tlist):
        c_ops = [self.photon_loss_lindblad()]
        result = mesolve([], initial_state, tlist, c_ops, [])
        return result.states


def compute_bit_flip_rate(cat_state, alpha_range, n_cavity=30, kappa=0.1):
    bit_flip_rates = []
    
    for alpha in alpha_range:
        cat = CatState(n_cavity, alpha)
        logical_zero = cat.logical_zero()
        logical_one = cat.logical_one()
        
        overlap = abs((logical_zero.dag() * logical_one).full()[0, 0])**2
        bit_flip_rate = overlap * kappa
        bit_flip_rates.append(bit_flip_rate)
    
    return np.array(bit_flip_rates)


def compute_phase_flip_rate(cat_state, alpha_range, n_cavity=30, kappa=0.1):
    phase_flip_rates = []
    
    for alpha in alpha_range:
        avg_photon_number = alpha**2
        phase_flip_rate = kappa * avg_photon_number
        phase_flip_rates.append(phase_flip_rate)
    
    return np.array(phase_flip_rates)


def plot_biased_noise(alpha_range, bit_flip_rates, phase_flip_rates, 
                      save_path=None):
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.semilogy(alpha_range**2, bit_flip_rates, 'b-', linewidth=2, 
                label='Bit-flip rate')
    ax.plot(alpha_range**2, phase_flip_rates, 'r--', linewidth=2, 
            label='Phase-flip rate')
    
    ax.set_xlabel('Average photon number $|\\alpha|^2$')
    ax.set_ylabel('Error rate')
    ax.set_title('Biased Noise Profile of Cat Qubits')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()


def simulate_noise_dynamics(cat_state, alpha, n_cavity=30, kappa=0.1, 
                            t_max=10, n_steps=100, save_path=None):
    noise = NoiseModel(n_cavity, kappa)
    cat = CatState(n_cavity, alpha)
    initial_state = cat.logical_zero()
    
    tlist = np.linspace(0, t_max, n_steps)
    states = noise.evolve_state(initial_state, tlist)
    
    fidelities = []
    for state in states:
        fidelity = abs((initial_state.dag() * state).full()[0, 0])**2
        fidelities.append(fidelity)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(tlist, fidelities, 'b-', linewidth=2)
    ax.set_xlabel('Time')
    ax.set_ylabel('State fidelity')
    ax.set_title(f'Cat State Decay under Photon Loss ($\\alpha$={alpha:.1f})')
    ax.grid(True, alpha=0.3)
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()
    
    return tlist, fidelities
