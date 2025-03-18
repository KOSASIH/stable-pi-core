# quantum_processing/quantum_utils.py

import numpy as np
from qiskit import QuantumCircuit, Aer, execute
import logging

# Configure logging for Quantum Utilities
logger = logging.getLogger(__name__)

def create_quantum_circuit(num_qubits):
    """Create a quantum circuit with the specified number of qubits."""
    circuit = QuantumCircuit(num_qubits)
    logger.info(f"Created a quantum circuit with {num_qubits} qubits.")
    return circuit

def apply_hadamard(circuit, qubit_index):
    """Apply a Hadamard gate to the specified qubit."""
    circuit.h(qubit_index)
    logger.info(f"Applied Hadamard gate to qubit {qubit_index}.")

def measure_circuit(circuit):
    """Measure all qubits in the circuit."""
    circuit.measure_all()
    logger.info("All qubits measured.")

def execute_circuit(circuit):
    """Execute the quantum circuit and return the results."""
    backend = Aer.get_backend('qasm_simulator')
    job = execute(circuit, backend, shots=1024)
    result = job.result()
    counts = result.get_counts(circuit)
    logger.info(f"Circuit execution result: {counts}")
    return counts

def prepare_superposition_state(circuit, qubit_index):
    """Prepare a superposition state on the specified qubit."""
    apply_hadamard(circuit, qubit_index)

def prepare_entangled_state(circuit, qubit1_index, qubit2_index):
    """Prepare a Bell state (entangled state) between two qubits."""
    apply_hadamard(circuit, qubit1_index)
    circuit.cx(qubit1_index, qubit2_index)
    logger.info(f"Prepared entangled state between qubits {qubit1_index} and {qubit2_index}.")

def get_state_vector(counts):
    """Get the state vector from the measurement counts."""
    total_shots = sum(counts.values())
    state_vector = {key: value / total_shots for key, value in counts.items()}
    logger.info(f"State vector obtained: {state_vector}")
    return state_vector

# Example usage of the utility functions
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Create a quantum circuit with 2 qubits
    circuit = create_quantum_circuit(2)
    
    # Prepare an entangled state
    prepare_entangled_state(circuit, 0, 1)
    
    # Measure the circuit
    measure_circuit(circuit)
    
    # Execute the circuit
    counts = execute_circuit(circuit)
    
    # Get the state vector
    state_vector = get_state_vector(counts)
    logger.info(f"Final state vector: {state_vector}")
