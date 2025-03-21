# wdb/predictive_algorithm.py

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from .logger import Logger

class PredictiveAlgorithm:
    def __init__(self):
        self.models = {
            'linear_regression': LinearRegression(),
            'random_forest': RandomForestRegressor(),
            'gradient_boosting': GradientBoostingRegressor()
        }
        self.best_model = None
        self.logger = Logger()
        self.scaler = StandardScaler()

    def preprocess_data(self, historical_data):
        """
        Preprocesses the historical data for training.
        
        Args:
            historical_data (pd.DataFrame): The historical data to preprocess.

        Returns:
            X (np.ndarray): Features for training.
            y (np.ndarray): Target variable for training.
        """
        # Handle missing values
        historical_data.fillna(method='ffill', inplace=True)

        # Normalize features
        X = historical_data[['time']].values
        y = historical_data['data_volume'].values
        X = self.scaler.fit_transform(X)

        self.logger.log("Data preprocessing completed.")
        return X, y

    def train(self, historical_data):
        """
        Trains multiple models on the historical data and selects the best one.
        
        Args:
            historical_data (pd.DataFrame): The historical data for training.
        """
        X, y = self.preprocess_data(historical_data)
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

        best_mse = float('inf')
        for model_name, model in self.models.items():
            model.fit(X_train, y_train)
            predictions = model.predict(X_val)
            mse = mean_squared_error(y_val, predictions)
            self.logger.log(f"{model_name} MSE: {mse:.4f}")

            if mse < best_mse:
                best_mse = mse
                self.best_model = model_name
                self.logger.log(f"New best model found: {model_name} with MSE: {mse:.4f}")

    def predict(self, future_time):
        """
        Predicts future data needs based on the best trained model.
        
        Args:
            future_time (list): List of future time points for prediction.

        Returns:
            np.ndarray: Predicted data volumes.
        """
        if self.best_model is None:
            self.logger.log("No model trained yet. Please train the model first.")
            return None

        # Prepare future data for prediction
        future_data = np.array(future_time).reshape(-1, 1)
        future_data = self.scaler.transform(future_data)

        if self.best_model == 'linear_regression':
            model = self.models['linear_regression']
        elif self.best_model == 'random_forest':
            model = self.models['random_forest']
        elif self.best_model == 'gradient_boosting':
            model = self.models['gradient_boosting']

        predictions = model.predict(future_data)
        self.logger.log(f"Predictions for {future_time}: {predictions}")
        return predictions

    def get_best_model(self):
        """
        Returns the name of the best trained model.
        
        Returns:
            str: The name of the best model.
        """
        return self.best_model
