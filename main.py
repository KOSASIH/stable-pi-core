import logging
import os
import pandas as pd
import yaml
from algorithms.supply_adjustment import SupplyAdjustment
from algorithms.asset_management import AssetManagement
from algorithms.prediction_model import DemandPredictionModel

def load_config(env='development'):
    """Load configuration from the specified environment."""
    config_file = f'config/{env}.yaml'
    try:
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
        logging.info(f'Loaded configuration for {env} environment.')
        return config
    except FileNotFoundError:
        logging.error(f'Configuration file {config_file} not found.')
        raise
    except yaml.YAMLError as e:
        logging.error(f'Error parsing YAML configuration: {e}')
        raise

def initialize_algorithms(config):
    """Initialize the algorithms with the loaded configuration."""
    supply_adjuster = SupplyAdjustment()
    asset_manager = AssetManagement()
    demand_model = DemandPredictionModel()

    # Load historical data for training
    try:
        historical_data = pd.read_csv(config['data']['historical_data_path'])
        supply_adjuster.train_model(historical_data)
        asset_manager.train_model(historical_data)
        demand_model.train_model(historical_data)
        logging.info('Successfully trained models with historical data.')
    except Exception as e:
        logging.error(f'Error loading historical data: {e}')
        raise

    return supply_adjuster, asset_manager, demand_model

def predict_demand(demand_model, market_price, current_supply, other_factors):
    """Predict demand based on market conditions."""
    try:
        predicted_demand = demand_model.predict_demand(market_price, current_supply, other_factors)
        logging.info(f'Predicted Demand: {predicted_demand}')
        return predicted_demand
    except Exception as e:
        logging.error(f'Error predicting demand: {e}')
        raise

def adjust_allocations(asset_manager, current_allocations, market_conditions):
    """Adjust asset allocations based on predicted performance."""
    try:
        new_allocations = asset_manager.adjust_allocation(current_allocations, market_conditions)
        logging.info(f'Adjusted Allocations: {new_allocations}')
        return new_allocations
    except Exception as e:
        logging.error(f'Error adjusting allocations: {e}')
        raise

def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Load configuration
    environment = os.getenv('APP_ENV', 'development')  # Default to development
    config = load_config(environment)

    # Initialize algorithms
    supply_adjuster, asset_manager, demand_model = initialize_algorithms(config)

    # Example usage of the models
    market_price = 105
    current_supply = 1000
    other_factors = 1

    # Predict demand
    predicted_demand = predict_demand(demand_model, market_price, current_supply, other_factors)

    # Current allocations
    current_allocations = {'Asset_A': 1000, 'Asset_B': 1100}
    
    # Adjust allocations based on market conditions
    market_conditions = 1  # Example market condition
    new_allocations = adjust_allocations(asset_manager, current_allocations, market_conditions)

    # Log final allocations
    logging.info(f'Final Allocations: {new_allocations}')

if __name__ == "__main__":
    main()
