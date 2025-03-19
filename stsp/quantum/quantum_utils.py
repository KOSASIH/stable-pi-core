# stsp/quantum/quantum_utils.py

import logging
import random

def generate_random_qubit():
    """
    Generate a random qubit state (0 or 1).

    :return: A random qubit state.
    """
    qubit = random.choice([0, 1])
    logging.info("Generated random qubit: %s", qubit)
    return qubit

def measure_qubit(qubit):
    """
    Simulate measuring a qubit.

    :param qubit: The qubit state to measure (0 or 1).
    :return: The measured state of the qubit.
    """
    logging.info("Measuring qubit: %s", qubit)
    return qubit  # In a real implementation, this would involve quantum measurement

def entangle_qubits(qubit1, qubit2):
    """
    Simulate entangling two qubits.

    :param qubit1: The first qubit.
    :param qubit2: The second qubit.
    :return: A tuple representing the entangled state.
    """
    logging.info("Entangling qubits: %s and %s", qubit1, qubit2)
    # In a real implementation, this would create an entangled state
    return (qubit1, qubit2)

# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Generate a random qubit
    qubit = generate_random_qubit()

    # Measure the qubit
    measured_state = measure_qubit(qubit)
    print(f"Measured Qubit State: {measured_state}")

    # Entangle two qubits
    entangled_state = entangle_qubits(0, 1)
    print(f"Entangled Qubits: {entangled_state}")
