# ml/inference.py

import numpy as np
import logging
from .model import SimpleLinearRegression, RidgeRegression

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def make_prediction(model, X):
    """Make predictions using the trained model.

    Args:
        model (object): Trained model instance (SimpleLinearRegression or RidgeRegression).
        X (array-like): New feature data for prediction.

    Returns:
        array: Predicted values.
    """
    if not hasattr(model, 'predict'):
        raise ValueError("The provided model does not have a predict method.")
    
    predictions = model.predict(X)
    logging.info("Predictions made successfully.")
    return predictions

def predict_with_confidence(model, X, confidence=0.95):
    """Make predictions with confidence intervals.

    Args:
        model (object): Trained model instance (SimpleLinearRegression or RidgeRegression).
        X (array-like): New feature data for prediction.
        confidence (float): Confidence level for the interval (default is 0.95).

    Returns:
        tuple: Predicted values and confidence intervals (lower, upper).
    """
    if not hasattr(model, 'predict'):
        raise ValueError("The provided model does not have a predict method.")
    
    predictions = model.predict(X)
    
    # Calculate standard error of the predictions
    if hasattr(model, 'get_coefficients'):
        coefficients, intercept = model.get_coefficients()
        # Assuming a simple linear regression model for standard error calculation
        # This is a simplified approach; in practice, you would need to calculate
        # the standard error based on the residuals and the design matrix.
        standard_error = np.std(predictions) / np.sqrt(len(predictions))
    else:
        raise ValueError("Model does not support confidence interval calculation.")
    
    # Calculate the margin of error
    z_score = 1.96  # For 95% confidence
    margin_of_error = z_score * standard_error
    
    # Calculate confidence intervals
    lower_bound = predictions - margin_of_error
    upper_bound = predictions + margin_of_error
    
    logging.info("Predictions with confidence intervals made successfully.")
    return predictions, (lower_bound, upper_bound)

# Example usage
if __name__ == "__main__":
    # Sample data for demonstration
    model = SimpleLinearRegression()
    X_train = np.array([[1], [2], [3], [4], [5]])
    y_train = np.array([2, 3, 5, 7, 11])
    model.fit(X_train, y_train)

    # New data for prediction
    X_new = np.array([[6], [7], [8]])
    
    # Make predictions
    predictions = make_prediction(model, X_new)
    print("Predictions:", predictions)

    # Make predictions with confidence intervals
    predictions, confidence_intervals = predict_with_confidence(model, X_new)
    print("Predictions with Confidence Intervals:", predictions)
    print("Confidence Intervals:", confidence_intervals)
