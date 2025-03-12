# ml/__init__.py

"""
Machine Learning Module

This module provides functionalities for training and inference of machine learning models.
It includes a simple linear regression model, training routines, and prediction capabilities.
"""

from .model import SimpleLinearRegression
from .training import train_model
from .inference import make_prediction

__all__ = [
    "SimpleLinearRegression",  # Class for simple linear regression model
    "train_model",             # Function to train the model
    "make_prediction"          # Function to make predictions using the trained model
]

def version():
    """Return the version of the ML module."""
    return "1.0.0"

def description():
    """Return a brief description of the ML module."""
    return "This module implements basic machine learning functionalities including training and inference for linear regression models."
