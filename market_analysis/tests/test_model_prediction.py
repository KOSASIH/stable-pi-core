# tests/test_model_prediction.py

import pytest
import pandas as pd
from src.model_prediction import load_model, predict

def test_load_model():
    model = load_model('../models/price_prediction_model.pkl')
    assert model is not None, "The loaded model should not be None"

def test_predict():
    # Create a sample model and save it for testing
    from sklearn.linear_model import LinearRegression
    import joblib

    # Sample training data
    X_train = pd.DataFrame({'feature1': [1.0, 1.5], 'feature2': [2.0, 2.5]})
    y_train = pd.Series([10, 15])

    # Train a simple model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Save the model
    joblib.dump(model, '../models/test_price_prediction_model.pkl')

    # Load the model
    loaded_model = load_model('../models/test_price_prediction_model.pkl')

    # Prepare input data for prediction
    input_data = pd.DataFrame({'feature1': [2.0], 'feature2': [3.0]})

    # Make a prediction
    prediction = predict(loaded_model, input_data)

    # Check that the prediction is a numeric value
    assert isinstance(prediction, (float, int)), "Prediction should be a numeric value"
