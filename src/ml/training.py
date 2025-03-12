# ml/training.py

import numpy as np
from .model import SimpleLinearRegression, RidgeRegression
import joblib
import os

def train_model(model_type, X, y, alpha=None):
    """Train a machine learning model based on the specified type.

    Args:
        model_type (str): Type of model to train ('linear' or 'ridge').
        X (array-like): Feature data.
        y (array-like): Target data.
        alpha (float, optional): Regularization strength for Ridge Regression.

    Returns:
        object: Trained model instance.
    """
    if model_type == 'linear':
        model = SimpleLinearRegression()
    elif model_type == 'ridge':
        model = RidgeRegression(alpha=alpha)
    else:
        raise ValueError("Invalid model type. Choose 'linear' or 'ridge'.")

    model.fit(X, y)
    return model

def save_model(model, filename):
    """Save the trained model to a file.

    Args:
        model (object): Trained model instance.
        filename (str): Path to the file where the model will be saved.
    """
    joblib.dump(model, filename)
    print(f"Model saved to {filename}")

def load_model(filename):
    """Load a trained model from a file.

    Args:
        filename (str): Path to the file from which the model will be loaded.

    Returns:
        object: Loaded model instance.
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"No model found at {filename}")
    
    model = joblib.load(filename)
    print(f"Model loaded from {filename}")
    return model
