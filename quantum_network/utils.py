# quantum_network/utils.py

import numpy as np
import random
import hashlib

def generate_random_key(length: int) -> str:
    """
    Generate a random binary key of a specified length.

    Args:
        length (int): The length of the key to generate.

    Returns:
        str: A binary string representing the random key.
    """
    key = ''.join(random.choice('01') for _ in range(length))
    print(f"Generated random key: {key}")
    return key

def validate_message(expected: str, received: str) -> bool:
    """
    Validate that the received message matches the expected message.

    Args:
        expected (str): The expected message.
        received (str): The received message.

    Returns:
        bool: True if the messages match, False otherwise.
    """
    is_valid = expected == received
    print(f"Message validation: Expected '{expected}', Received '{received}', Valid: {is_valid}")
    return is_valid

def measure_qubit(qubit: np.ndarray) -> int:
    """
    Measure a qubit and collapse its state.

    Args:
        qubit (np.ndarray): The qubit to measure.

    Returns:
        int: The measurement result (0 or 1).
    """
    probabilities = np.abs(qubit) ** 2
    result = np.random.choice([0, 1], p=probabilities)
    print(f"Measured qubit {qubit} with result {result}.")
    return result

def hash_data(data: str) -> str:
    """
    Create a SHA-256 hash of the given data.

    Args:
        data (str): The data to hash.

    Returns:
        str: The SHA-256 hash of the data.
    """
    hashed = hashlib.sha256(data.encode()).hexdigest()
    print(f"Hashed data '{data}' to '{hashed}'.")
    return hashed

def create_entangled_pair() -> np.ndarray:
    """
    Create a Bell state (entangled pair of qubits).

    Returns:
        np.ndarray: The entangled qubit pair in Bell state.
    """
    # Create a Bell state (|00> + |11>) / sqrt(2)
    qubit_a = np.array([1, 0])  # |0>
    qubit_b = np.array([0, 1])  # |1>
    entangled_pair = (qubit_a + qubit_b) / np.sqrt(2)
    print(f"Created entangled pair: {entangled_pair}")
    return entangled_pair

# Example usage
if __name__ == "__main__":
    # Generate a random key
    random_key = generate_random_key(8)

    # Validate a message
    validate_message("Hello", "Hello")
    validate_message("Hello", "World")

    # Measure a qubit
    qubit = np.array([0.707, 0.707])  # Example qubit in superposition
    measure_qubit(qubit)

    # Hash some data
    hash_data("Quantum Network Data")

    # Create an entangled pair
    create_entangled_pair()
