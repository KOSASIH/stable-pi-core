import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
import joblib
import logging
import yaml

class AssetManagement:
    def __init__(self, config_path='config.yaml'):
        self.model = None
        self.load_config(config_path)
        self.load_model(self.model_path)

    def load_config(self, config_path):
        """Load configuration from a YAML file."""
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            self.model_path = config.get('asset_model_path', 'asset_management_model.pkl')
            self.test_size = config.get('test_size', 0.2)

    def load_model(self, model_path):
        """Load a pre-trained machine learning model."""
        try:
            self.model = joblib.load(model_path)
            logging.info(f'Model loaded from {model_path}')
        except FileNotFoundError:
            logging.warning(f'Model file not found at {model_path}. Please train the model first.')

    def train_model(self, historical_data):
        """Train a Gradient Boosting model on historical asset performance data."""
        # Prepare the data
        X = historical_data[['market_conditions', 'current_allocation', 'risk_factors']]
        y = historical_data['asset_performance']

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=self.test_size, random_state=42)

        # Train the model
        self.model = GradientBoostingClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)

        # Save the model
        joblib.dump(self.model, self.model_path)
        logging.info(f'Model trained and saved to {self.model_path}')

        # Evaluate the model
        score = self.model.score(X_test, y_test)
        logging.info(f'Model trained with accuracy score: {score}')

    def predict_asset_performance(self, market_conditions, current_allocation, risk_factors):
        """Predict asset performance based on market conditions."""
        if self.model is None:
            raise Exception("Model is not trained or loaded.")

        # Prepare input for prediction
        input_data = np.array([[market_conditions, current_allocation, risk_factors]])
        predicted_performance = self.model.predict(input_data)
        logging.info(f'Predicted asset performance: {predicted_performance[0]}')
        return predicted_performance[0]

    def assess_risk(self, current_allocations):
        """Assess risk based on current allocations and market conditions."""
        # Placeholder for risk assessment logic
        # For example, you could calculate volatility based on historical price data
        risk_score = np.random.rand()  # Simulated risk score for demonstration
        logging.info(f'Assessed risk score: {risk_score}')
        return risk_score

    def adjust_allocation(self, current_allocations, market_conditions):
        """Adjust asset allocations based on predicted performance and risk assessment."""
        new_allocations = current_allocations.copy()
        risk_score = self.assess_risk(current_allocations)

        for asset in current_allocations.keys():
            predicted_performance = self.predict_asset_performance(market_conditions, current_allocations[asset], risk_score)
            adjustment_factor = 0.05  # 5% adjustment

            if predicted_performance == 1:  # Assuming 1 indicates good performance
                new_allocations[asset] += adjustment_factor * current_allocations[asset]  # Increase allocation
            else:
                new_allocations[asset] -= adjustment_factor * current_allocations[asset]  # Decrease allocation

            new_allocations[asset] = max(new_allocations[asset], 0)  # Ensure allocation is not negative

        logging.info(f'New asset allocations: {new_allocations}')
        return new_allocations

# Example usage
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Load historical data (this should be replaced with actual data)
    historical_data = pd.DataFrame({
        'market_conditions': [1, 2, 1, 2, 1],
        'current_allocation': [1000, 1100, 1200, 900, 800],
        'risk_factors': [1, 2, 1, 2, 1],
        'asset_performance': [1, 0, 1, 0, 1]  # 1 for good performance, 0 for poor performance
    })

    # Initialize the asset management algorithm
    asset_manager = AssetManagement()

    # Train the model
    asset_manager.train_model(historical_data)

    # Current allocations
    current_allocations = {
        'Asset_A': 1000,
        'Asset_B': 1100,
        'Asset_C': 1200
    }

    # Predict and adjust allocations based on market conditions
    market_conditions = 2
    new_allocations = asset_manager.adjust_allocation(current_allocations, market_conditions)
    print(f'Adjusted Allocations: {new_allocations}')
