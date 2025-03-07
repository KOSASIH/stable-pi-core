# src/model_evaluation.py

import pandas as pd
import numpy as np
import joblib
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt

def evaluate_model(model_path, data_path):
    """Evaluate the performance of the price prediction model."""
    # Load the model
    model = joblib.load(model_path)

    # Load the data
    df = pd.read_csv(data_path)
    X = df.index.values.reshape(-1, 1)  # Use index as feature
    y_true = df['price'].values  # True target values

    # Make predictions
    y_pred = model.predict(X)

    # Calculate evaluation metrics
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)

    # Print the evaluation results
    print(f'Mean Absolute Error (MAE): {mae:.2f}')
    print(f'Mean Squared Error (MSE): {mse:.2f}')
    print(f'R² Score: {r2:.2f}')

    # Visualize the results
    visualize_results(df['date'], y_true, y_pred)

def visualize_results(dates, y_true, y_pred):
    """Visualize the actual vs predicted prices."""
    plt.figure(figsize=(14, 7))
    plt.plot(dates, y_true, label='Actual Prices', color='blue', alpha=0.6)
    plt.plot(dates, y_pred, label='Predicted Prices', color='orange', alpha=0.6)
    plt.title('Actual vs Predicted Prices')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    evaluate_model('models/price_prediction_model.pkl', 'data/processed_data.csv')
