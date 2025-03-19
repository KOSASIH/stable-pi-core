import numpy as np
import random
import logging

# Configure logging
logging.basicConfig(filename='quantum_interface.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class QuantumInterface:
    def __init__(self):
        """
        Initialize the Quantum Interface for interacting with quantum systems.
        """
        self.quantum_state = None  # Placeholder for the quantum state
        logging.info("Quantum Interface initialized.")

    def prepare_quantum_state(self, state_vector):
        """
        Prepare a quantum state given a state vector.
        
        :param state_vector: A list or numpy array representing the quantum state.
        """
        if not self.is_valid_state_vector(state_vector):
            logging.error("Invalid state vector provided.")
            raise ValueError("Invalid state vector. Must be a normalized vector.")
        
        self.quantum_state = np.array(state_vector)
        logging.info(f"Quantum state prepared: {self.quantum_state}")

    def is_valid_state_vector(self, state_vector):
        """
        Check if the provided state vector is valid (normalized).
        
        :param state_vector: A list or numpy array representing the quantum state.
        :return: True if valid, False otherwise.
        """
        norm = np.linalg.norm(state_vector)
        return np.isclose(norm, 1.0)

    def measure_quantum_state(self):
        """
        Simulate a measurement of the quantum state.
        
        :return: The result of the measurement.
        """
        if self.quantum_state is None:
            logging.error("Quantum state is not prepared.")
            raise RuntimeError("Quantum state is not prepared.")
        
        probabilities = np.abs(self.quantum_state) ** 2
        measurement_result = np.random.choice(len(self.quantum_state), p=probabilities)
        logging.info(f"Quantum measurement result: {measurement_result}")
        return measurement_result

    def entangle_states(self, state1, state2):
        """
        Simulate the entanglement of two quantum states.
        
        :param state1: First quantum state.
        :param state2: Second quantum state.
        :return: A new entangled state.
        """
        if not self.is_valid_state_vector(state1) or not self.is_valid_state_vector(state2):
            logging.error("Invalid state vectors provided for entanglement.")
            raise ValueError("Both states must be valid normalized vectors.")
        
        # Simple entanglement simulation (not physically accurate)
        entangled_state = np.kron(state1, state2)  # Kronecker product
        logging.info(f"Entangled state created: {entangled_state}")
        return entangled_state

    def reset_quantum_state(self):
        """
        Reset the quantum state to None.
        """
        self.quantum_state = None
        logging.info("Quantum state reset.")

if __name__ == "__main__":
    # Example usage of the QuantumInterface
    qi = QuantumInterface()
    try:
        # Prepare a quantum state
        state_vector = [1/np.sqrt(2), 1/np.sqrt(2)]  # Example: |+> state
        qi.prepare_quantum_state(state_vector)

        # Measure the quantum state
        result = qi.measure_quantum_state()
        print(f"Measurement Result: {result}")

        # Entangle two states
        state1 = [1, 0]  # |0>
        state2 = [0, 1]  # |1>
        entangled = qi.entangle_states(state1, state2)
        print(f"Entangled State: {entangled}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        qi.reset_quantum_state()
