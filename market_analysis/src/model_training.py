# src/model_training.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

def train_model(data_path):
    """Train a price prediction model."""
    df = pd.read_csv(data_path)
    X = df.index.values.reshape(-1, 1)  # Use index as feature
    y = df['price'].values  # Target variable

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create and train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Save the model
    joblib.dump(model, 'models/price_prediction_model.pkl')
    print("Model trained and saved as price_prediction_model.pkl")

if __name__ == "__main__":
    train_model('data/processed_data.csv')
