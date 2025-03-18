# pqpn/utils.py

import yaml
import logging
import numpy as np
import os

# Configure logging for utility functions
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config(config_file):
    """
    Load configuration from a YAML file.

    :param config_file: Path to the YAML configuration file.
    :return: Configuration dictionary.
    """
    if not os.path.exists(config_file):
        logger.error("Configuration file not found: %s", config_file)
        raise FileNotFoundError(f"Configuration file not found: {config_file}")

    try:
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
            logger.info("Configuration loaded successfully from %s", config_file)
            return config
    except yaml.YAMLError as e:
        logger.error("Error parsing YAML configuration file: %s", e)
        raise
    except Exception as e:
        logger.error("Error loading configuration file: %s", e)
        raise

def save_to_file(data, filename):
    """
    Save data to a file.

    :param data: Data to be saved (can be a string, list, dict, etc.).
    :param filename: Path to the file where data will be saved.
    """
    try:
        with open(filename, 'w') as file:
            if isinstance(data, (list, dict)):
                yaml.dump(data, file)
            else:
                file.write(str(data))
            logger.info("Data saved successfully to %s", filename)
    except Exception as e:
        logger.error("Error saving data to file: %s", e)
        raise

def generate_random_state(num_qubits):
    """
    Generate a random quantum state for a given number of qubits.

    :param num_qubits: Number of qubits.
    :return: Random quantum state as a normalized numpy array.
    """
    # Generate a random complex vector
    state_vector = np.random.rand(2 ** num_qubits) + 1j * np.random.rand(2 ** num_qubits)
    # Normalize the state vector
    norm = np.linalg.norm(state_vector)
    normalized_state = state_vector / norm
    logger.info("Generated random quantum state for %d qubits.", num_qubits)
    return normalized_state

def calculate_inner_product(state1, state2):
    """
    Calculate the inner product of two quantum states.

    :param state1: First quantum state (numpy array).
    :param state2: Second quantum state (numpy array).
    :return: Inner product as a complex number.
    """
    if state1.shape != state2.shape:
        logger.error("Quantum states must have the same shape for inner product.")
        raise ValueError("Quantum states must have the same shape for inner product.")
    
    inner_product = np.vdot(state1, state2)  # Conjugate transpose of state1
    logger.info("Calculated inner product.")
    return inner_product

def validate_quantum_state(state):
    """
    Validate a quantum state to ensure it is normalized.

    :param state: Quantum state (numpy array).
    :return: Boolean indicating whether the state is normalized.
    """
    norm = np.linalg.norm(state)
    is_normalized = np.isclose(norm, 1.0)
    logger.info("Quantum state validation: %s", "normalized" if is_normalized else "not normalized")
    return is_normalized

def create_directory(directory):
    """
    Create a directory if it does not exist.

    :param directory: Path to the directory to create.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info("Created directory: %s", directory)
    else:
        logger.info("Directory already exists: %s", directory)

# Example usage
if __name__ == "__main__":
    # Load configuration
    try:
        config = load_config("pqpn/pqpn_config.yaml")
    except Exception as e:
        logger.error("Failed to load configuration: %s", e)

    # Generate a random quantum state
    random_state = generate_random_state(2)

    # Validate the quantum state
    is_valid = validate_quantum_state(random_state)
    print(f"Is the generated state normalized? {is_valid}")

    # Calculate inner product with itself
    inner_product = calculate_inner_product(random_state, random_state)
    print(f"Inner product of the state with itself: {inner_product}")

    # Create a directory for results
    create_directory("results")
