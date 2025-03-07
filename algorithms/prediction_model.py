import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
import joblib
import logging
import yaml

class DemandPredictionModel:
    def __init__(self, config_path='config.yaml'):
        self.model = None
        self.load_config(config_path)
        self.load_model(self.model_path)

    def load_config(self, config_path):
        """Load configuration from a YAML file."""
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            self.model_path = config.get('demand_model_path', 'demand_prediction_model.pkl')
            self.test_size = config.get('test_size', 0.2)

    def load_model(self, model_path):
        """Load a pre-trained machine learning model."""
        try:
            self.model = joblib.load(model_path)
            logging.info(f'Model loaded from {model_path}')
        except FileNotFoundError:
            logging.warning(f'Model file not found at {model_path}. Please train the model first.')

    def train_model(self, historical_data):
        """Train a Gradient Boosting model on historical demand data."""
        # Prepare the data
        X = historical_data[['market_price', 'current_supply', 'other_factors']]
        y = historical_data['demand']

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=self.test_size, random_state=42)

        # Hyperparameter tuning using Grid Search
        param_grid = {
            'n_estimators': [100, 200],
            'learning_rate': [0.01, 0.1, 0.2],
            'max_depth': [3, 5, 7]
        }
        grid_search = GridSearchCV(GradientBoostingRegressor(), param_grid, cv=5)
        grid_search.fit(X_train, y_train)

        # Best model from grid search
        self.model = grid_search.best_estimator_
        logging.info(f'Best parameters: {grid_search.best_params_}')

        # Save the model
        joblib.dump(self.model, self.model_path)
        logging.info(f'Model trained and saved to {self.model_path}')

        # Evaluate the model
        score = self.model.score(X_test, y_test)
        logging.info(f'Model trained with R^2 score: {score}')

    def predict_demand(self, market_price, current_supply, other_factors):
        """Predict demand based on market conditions."""
        if self.model is None:
            raise Exception("Model is not trained or loaded.")

        # Prepare input for prediction
        input_data = np.array([[market_price, current_supply, other_factors]])
        predicted_demand = self.model.predict(input_data)
        logging.info(f'Predicted demand: {predicted_demand[0]}')
        return predicted_demand[0]

# Example usage
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Load historical data (this should be replaced with actual data)
    historical_data = pd.DataFrame({
        'market_price': [100, 105, 110, 95, 90],
        'current_supply': [1000, 1100, 1200, 900, 800],
        'other_factors': [1, 2, 1, 2, 1],
        'demand': [950, 1150, 1250, 850, 750]
    })

    # Initialize the demand prediction model
    demand_model = DemandPredictionModel()

    # Train the model
    demand_model.train_model(historical_data)

    # Predict demand based on current market conditions
    market_price = 105
    current_supply = 1000
    other_factors = 1
    predicted_demand = demand_model.predict_demand(market_price, current_supply, other_factors)
    print(f'Predicted Demand: {predicted_demand}')
