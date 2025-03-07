# src/utils.py

import joblib
import numpy as np
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_model(model_path):
    """Load the trained model from the specified path."""
    try:
        model = joblib.load(model_path)
        logging.info(f"Model loaded successfully from {model_path}")
        return model
    except Exception as e:
        logging.error(f"Error loading model: {e}")
        raise

def preprocess_input(input_data):
    """Preprocess the input data for prediction."""
    try:
        # Validate input data
        if not isinstance(input_data, (list, np.ndarray)):
            raise ValueError("Input data must be a list or numpy array.")
        
        # Convert input data to a numpy array and reshape for model input
        input_array = np.array(input_data).reshape(-1, 1)
        logging.info(f"Input data preprocessed: {input_array}")
        return input_array
    except Exception as e:
        logging.error(f"Error preprocessing input data: {e}")
        raise

def validate_input(input_data):
    """Validate the input data format."""
    if not isinstance(input_data, (list, np.ndarray)):
        raise ValueError("Input data must be a list or numpy array.")
    if len(input_data) == 0:
        raise ValueError("Input data cannot be empty.")
    logging.info("Input data validated successfully.")
