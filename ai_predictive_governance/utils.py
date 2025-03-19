import json
import os
from typing import Any, Dict

def load_config(config_file: str) -> Dict[str, Any]:
    """
    Loads configuration settings from a JSON file.

    Args:
        config_file (str): The path to the configuration file.

    Returns:
        Dict[str, Any]: A dictionary containing the configuration settings.
    """
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Configuration file not found: {config_file}")

    with open(config_file, 'r') as f:
        config = json.load(f)
    return config

def log_to_file(data: Dict[str, Any], log_file: str) -> None:
    """
    Logs data to a specified file in JSON format.

    Args:
        data (Dict[str, Any]): The data to log.
        log_file (str): The name of the file to log the data to.
    """
    with open(log_file, 'a') as f:
        f.write(json.dumps(data) + '\n')

def validate_data(data: Dict[str, Any], required_keys: List[str]) -> bool:
    """
    Validates that the provided data contains the required keys.

    Args:
        data (Dict[str, Any]): The data to validate.
        required_keys (List[str]): A list of required keys.

    Returns:
        bool: True if the data is valid, False otherwise.
    """
    for key in required_keys:
        if key not in data:
            print(f"Missing required key: {key}")
            return False
    return True

def save_predictions(predictions: List[Dict[str, Any]], output_file: str) -> None:
    """
    Saves predictions to a specified output file in JSON format.

    Args:
        predictions (List[Dict[str, Any]]): The predictions to save.
        output_file (str): The name of the file to save the predictions to.
    """
    with open(output_file, 'w') as f:
        json.dump(predictions, f, indent=4)

def load_predictions(input_file: str) -> List[Dict[str, Any]]:
    """
    Loads predictions from a specified input file in JSON format.

    Args:
        input_file (str): The name of the file to load predictions from.

    Returns:
        List[Dict[str, Any]]: A list of predictions loaded from the file.
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Input file not found: {input_file}")

    with open(input_file, 'r') as f:
        predictions = json.load(f)
    return predictions
