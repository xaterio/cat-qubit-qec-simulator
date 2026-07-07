import numpy as np
from qutip import tensor, basis, sigmaz, identity
from .cat_state import CatState


class RepetitionCode:
    def __init__(self, n_qubits, n_cavity, alpha):
        self.n_qubits = n_qubits
        self.n_cavity = n_cavity
        self.alpha = alpha
        self.cat = CatState(n_cavity, alpha)
        
    def encode_logical_zero(self):
        logical_zero = self.cat.logical_zero()
        encoded_state = tensor([logical_zero] * self.n_qubits)
        return encoded_state
    
    def encode_logical_one(self):
        logical_one = self.cat.logical_one()
        encoded_state = tensor([logical_one] * self.n_qubits)
        return encoded_state
    
    def stabilizer_generators(self):
        stabilizers = []
        for i in range(self.n_qubits - 1):
            op_list = [identity(self.n_cavity)] * self.n_qubits
            op_list[i] = sigmaz()
            op_list[i + 1] = sigmaz()
            stabilizer = tensor(op_list)
            stabilizers.append(stabilizer)
        return stabilizers
    
    def measure_syndrome(self, state):
        stabilizers = self.stabilizer_generators()
        syndrome = []
        
        for stabilizer in stabilizers:
            expectation = (state.dag() * stabilizer * state).tr()
            syndrome.append(np.sign(expectation.real))
        
        return syndrome
    
    def apply_phase_flip(self, state, qubit_index):
        op_list = [identity(self.n_cavity)] * self.n_qubits
        op_list[qubit_index] = sigmaz()
        phase_flip_op = tensor(op_list)
        return phase_flip_op * state
    
    def correct_errors(self, syndrome):
        correction = np.zeros(self.n_qubits)
        
        for i in range(len(syndrome)):
            if syndrome[i] == -1:
                correction[i] += 1
                if i + 1 < self.n_qubits:
                    correction[i + 1] += 1
        
        correction = correction % 2
        return correction
    
    def recovery_operation(self, state, correction):
        op_list = [identity(self.n_cavity)] * self.n_qubits
        for i, flip in enumerate(correction):
            if flip == 1:
                op_list[i] = sigmaz()
        recovery_op = tensor(op_list)
        return recovery_op * state
    
    def simulate_error_correction(self, initial_state, error_pattern):
        corrupted_state = initial_state
        for i, error in enumerate(error_pattern):
            if error == 1:
                corrupted_state = self.apply_phase_flip(corrupted_state, i)
        
        syndrome = self.measure_syndrome(corrupted_state)
        correction = self.correct_errors(syndrome)
        recovered_state = self.recovery_operation(corrupted_state, correction)
        
        return corrupted_state, recovered_state, syndrome, correction
    
    def logical_fidelity(self, state1, state2):
        overlap = abs((state1.dag() * state2).tr())**2
        return overlap


def simulate_qec_performance(n_qubits_list, alpha_values, n_cavity=30, 
                            n_trials=100):
    results = {}
    
    for n_qubits in n_qubits_list:
        for alpha in alpha_values:
            code = RepetitionCode(n_qubits, n_cavity, alpha)
            
            success_count = 0
            for _ in range(n_trials):
                logical_zero = code.encode_logical_zero()
                
                error_pattern = np.random.randint(0, 2, n_qubits)
                _, recovered_state, _, _ = code.simulate_error_correction(
                    logical_zero, error_pattern
                )
                
                fidelity = code.logical_fidelity(logical_zero, recovered_state)
                if fidelity > 0.99:
                    success_count += 1
            
            success_rate = success_count / n_trials
            results[(n_qubits, alpha)] = success_rate
    
    return results
