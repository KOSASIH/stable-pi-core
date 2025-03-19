# src/quantum_consensus/utils.py

import numpy as np
import random
import logging

# Set up logging for the utility functions
logger = logging.getLogger(__name__)

def generate_random_state(dimensions=2):
    """
    Generate a random quantum state.

    Parameters:
    - dimensions (int): The dimensions of the quantum state (default is 2 for a qubit).

    Returns:
    - np.ndarray: A normalized random quantum state.
    """
    state = np.random.rand(dimensions)
    normalized_state = state / np.linalg.norm(state)
    logger.info(f"Generated random quantum state: {normalized_state}")
    return normalized_state

def measure_state(state):
    """
    Measure a quantum state.

    Parameters:
    - state (np.ndarray): The quantum state to measure.

    Returns:
    - int: The result of the measurement (0 or 1 for a qubit).
    """
    probabilities = np.abs(state) ** 2
    measurement_result = np.random.choice(len(state), p=probabilities)
    logger.info(f"Measured state: {state}, Result: {measurement_result}")
    return measurement_result

def entangle_states(state1, state2):
    """
    Create an entangled state from two quantum states.

    Parameters:
    - state1 (np.ndarray): The first quantum state.
    - state2 (np.ndarray): The second quantum state.

    Returns:
    - np.ndarray: The resulting entangled state.
    """
    # Simple tensor product to create an entangled state
    entangled_state = np.kron(state1, state2)
    logger.info(f"Created entangled state from {state1} and {state2}: {entangled_state}")
    return entangled_state

def apply_unitary(state, unitary):
    """
    Apply a unitary operation to a quantum state.

    Parameters:
    - state (np.ndarray): The quantum state to which the unitary is applied.
    - unitary (np.ndarray): The unitary matrix to apply.

    Returns:
    - np.ndarray: The resulting quantum state after applying the unitary.
    """
    new_state = np.dot(unitary, state)
    logger.info(f"Applied unitary: {unitary} to state: {state}, Resulting state: {new_state}")
    return new_state

def random_unitary(dimensions=2):
    """
    Generate a random unitary matrix.

    Parameters:
    - dimensions (int): The dimensions of the unitary matrix (default is 2 for a qubit).

    Returns:
    - np.ndarray: A random unitary matrix.
    """
    # Generate a random unitary matrix using QR decomposition
    random_matrix = np.random.rand(dimensions, dimensions)
    q, r = np.linalg.qr(random_matrix)
    unitary = q * (np.diag(np.sign(np.diag(r))))  # Ensure the unitary is properly normalized
    logger.info(f"Generated random unitary matrix: {unitary}")
    return unitary
