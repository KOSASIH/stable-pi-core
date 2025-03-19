# tests/test_model_training.py

import pytest
import pandas as pd
from src.model_training import train_model

def test_train_model():
    # Create a sample DataFrame for testing
    sample_data = {
        'feature1': [1.0, 1.5, 2.0, 2.5, 3.0],
        'feature2': [2.0, 2.5, 3.0, 3.5, 4.0],
        'target': [10, 15, 20, 25, 30]
    }
    df = pd.DataFrame(sample_data)

    # Train the model
    model = train_model(df)

    # Check that the model is not None
    assert model is not None, "The trained model should not be None"
