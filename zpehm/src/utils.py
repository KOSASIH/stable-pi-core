import numpy as np
import logging

# Configure logging
logging.basicConfig(filename='utils.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def joules_to_electronvolts(joules):
    """
    Convert energy from Joules to electronvolts.
    
    :param joules: Energy in Joules.
    :return: Energy in electronvolts.
    """
    electronvolt = 1.60218e-19  # Joules per electronvolt
    eV = joules / electronvolt
    logging.info(f"Converted {joules:.6e} Joules to {eV:.6e} eV")
    return eV

def electronvolts_to_joules(electronvolts):
    """
    Convert energy from electronvolts to Joules.
    
    :param electronvolts: Energy in electronvolts.
    :return: Energy in Joules.
    """
    electronvolt = 1.60218e-19  # Joules per electronvolt
    joules = electronvolts * electronvolt
    logging.info(f"Converted {electronvolts:.6e} eV to {joules:.6e} Joules")
    return joules

def normalize_vector(vector):
    """
    Normalize a vector.
    
    :param vector: A list or numpy array representing the vector.
    :return: A normalized vector.
    """
    norm = np.linalg.norm(vector)
    if norm == 0:
        logging.error("Cannot normalize a zero vector.")
        raise ValueError("Cannot normalize a zero vector.")
    normalized_vector = vector / norm
    logging.info(f"Normalized vector: {normalized_vector}")
    return normalized_vector

def mean(values):
    """
    Calculate the mean of a list of values.
    
    :param values: A list of numerical values.
    :return: The mean of the values.
    """
    if not values:
        logging.error("Mean calculation requires at least one value.")
        raise ValueError("Mean calculation requires at least one value.")
    mean_value = np.mean(values)
    logging.info(f"Calculated mean: {mean_value:.6f}")
    return mean_value

def variance(values):
    """
    Calculate the variance of a list of values.
    
    :param values: A list of numerical values.
    :return: The variance of the values.
    """
    if not values:
        logging.error("Variance calculation requires at least one value.")
        raise ValueError("Variance calculation requires at least one value.")
    variance_value = np.var(values)
    logging.info(f"Calculated variance: {variance_value:.6f}")
    return variance_value

def log_message(message):
    """
    Log a message to the log file.
    
    :param message: The message to log.
    """
    logging.info(message)

if __name__ == "__main__":
    # Example usage of the utility functions
    try:
        joules = 1.0
        eV = joules_to_electronvolts(joules)
        joules_converted_back = electronvolts_to_joules(eV)

        vector = np.array([3, 4])
        normalized_vector = normalize_vector(vector)

        values = [1, 2, 3, 4, 5]
        mean_value = mean(values)
        variance_value = variance(values)

        log_message("Utility functions executed successfully.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
