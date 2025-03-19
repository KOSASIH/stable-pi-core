# ml/model.py

from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

class SimpleLinearRegression:
    def __init__(self):
        """Initialize the Simple Linear Regression model."""
        self.model = LinearRegression()

    def fit(self, X, y):
        """Train the model using the provided features and target.

        Args:
            X (array-like): Feature data.
            y (array-like): Target data.
        """
        self.model.fit(X, y)

    def predict(self, X):
        """Make predictions using the trained model.

        Args:
            X (array-like): New feature data for prediction.

        Returns:
            array: Predicted values.
        """
        return self.model.predict(X)

    def get_coefficients(self):
        """Return the coefficients of the trained model.

        Returns:
            tuple: Coefficients and intercept of the model.
        """
        return self.model.coef_, self.model.intercept_

    def evaluate(self, X, y):
        """Evaluate the model using Mean Squared Error and R-squared.

        Args:
            X (array-like): Feature data for evaluation.
            y (array-like): True target values.

        Returns:
            dict: Evaluation metrics including MSE and R².
        """
        predictions = self.predict(X)
        mse = mean_squared_error(y, predictions)
        r2 = r2_score(y, predictions)
        return {"Mean Squared Error": mse, "R-squared": r2}


class RidgeRegression:
    def __init__(self, alpha=1.0):
        """Initialize the Ridge Regression model.

        Args:
            alpha (float): Regularization strength; must be a positive float.
        """
        self.model = Ridge(alpha=alpha)

    def fit(self, X, y):
        """Train the Ridge Regression model using the provided features and target.

        Args:
            X (array-like): Feature data.
            y (array-like): Target data.
        """
        self.model.fit(X, y)

    def predict(self, X):
        """Make predictions using the trained Ridge Regression model.

        Args:
            X (array-like): New feature data for prediction.

        Returns:
            array: Predicted values.
        """
        return self.model.predict(X)

    def get_coefficients(self):
        """Return the coefficients of the trained Ridge Regression model.

        Returns:
            tuple: Coefficients and intercept of the model.
        """
        return self.model.coef_, self.model.intercept_

    def evaluate(self, X, y):
        """Evaluate the Ridge Regression model using Mean Squared Error and R-squared.

        Args:
            X (array-like): Feature data for evaluation.
            y (array-like): True target values.

        Returns:
            dict: Evaluation metrics including MSE and R².
        """
        predictions = self.predict(X)
        mse = mean_squared_error(y, predictions)
        r2 = r2_score(y, predictions)
        return {"Mean Squared Error": mse, "R-squared": r2}
