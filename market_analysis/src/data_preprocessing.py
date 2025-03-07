# src/data_preprocessing.py

import pandas as pd
import numpy as np

def generate_synthetic_data(num_samples=1000):
    """Generate synthetic market data for price prediction."""
    np.random.seed(42)
    dates = pd.date_range(start='2020-01-01', periods=num_samples)
    prices = np.random.rand(num_samples) * 100  # Random prices between 0 and 100
    return pd.DataFrame({'date': dates, 'price': prices})

def preprocess_data(df):
    """Preprocess the data for training."""
    df['price'] = df['price'].shift(-1)  # Shift prices for prediction
    df.dropna(inplace=True)  # Remove NaN values
    return df

if __name__ == "__main__":
    # Generate and preprocess data
    data = generate_synthetic_data()
    processed_data = preprocess_data(data)
    processed_data.to_csv('data/processed_data.csv', index=False)
    print("Synthetic data generated and preprocessed.")
