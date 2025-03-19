import numpy as np
import pandas as pd
from typing import Dict, Any, List
from .model import PredictiveModel

def generate_recommendations(model: PredictiveModel, data: pd.DataFrame, target_column: str, num_recommendations: int = 5) -> List[Dict[str, Any]]:
    """
    Generates recommendations based on the predictions from the trained model.

    Args:
        model (PredictiveModel): The trained predictive model.
        data (pd.DataFrame): The preprocessed data for making predictions.
        target_column (str): The name of the target column for prediction.
        num_recommendations (int): The number of recommendations to generate.

    Returns:
        List[Dict[str, Any]]: A list of recommendations based on the model's predictions.
    """
    # Prepare the data for predictions
    X, _ = model.prepare_data(data, target_column)

    # Generate predictions
    predictions = model.model.predict(X)

    # Create recommendations based on predictions
    recommendations = []
    for i in range(len(predictions) - 1):
        recommendation = {
            "current_value": data[target_column].iloc[i],
            "predicted_value": predictions[i + 1][0],
            "recommendation": "Increase" if predictions[i + 1][0] > data[target_column].iloc[i] else "Decrease"
        }
        recommendations.append(recommendation)

    # Limit the number of recommendations
    return recommendations[:num_recommendations]

def log_prediction_results(predictions: List[Dict[str, Any]], log_file: str) -> None:
    """
    Logs the prediction results to a specified log file.

    Args:
        predictions (List[Dict[str, Any]]): The list of predictions to log.
        log_file (str): The path to the log file.
    """
    with open(log_file, 'a') as f:
        for prediction in predictions:
            f.write(f"{prediction}\n")
