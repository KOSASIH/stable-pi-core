# src/model_prediction.py

import joblib
import numpy as np

def make_prediction(model_path, input_data):
    """Make a price prediction using the trained model."""
    model = joblib.load(model_path)
    prediction = model.predict(input_data)
    return prediction

if __name__ == "__main__":
    # Example input data (e.g., the next index value)
    input_data = np.array([[1000]])  # Replace with the appropriate input
    predicted_price = make_prediction('models/price_prediction_model.pkl', input_data)
    print(f'Predicted price: {predicted_price[0]:.2f}')
