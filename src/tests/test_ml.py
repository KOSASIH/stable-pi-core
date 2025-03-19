# tests/test_ml.py

import pytest
from ml.model import MLModel  # Assuming you have an MLModel class

@pytest.fixture
def ml_model():
    model = MLModel()
    model.train()  # Assuming there's a train method
    return model

def test_model_inference(ml_model):
    input_data = [1, 2, 3]  # Example input data
    prediction = ml_model.infer(input_data)  # Assuming there's an infer method
    assert prediction is not None
    assert isinstance(prediction, float)  # Assuming the output is a float
