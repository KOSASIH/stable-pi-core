import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

class PredictiveModel:
    """
    A class to define, train, and evaluate a predictive model for AI-driven governance.

    Attributes:
        model (Sequential): The LSTM model instance.
        input_shape (tuple): The shape of the input data for the model.
    """

    def __init__(self, input_shape: tuple):
        self.model = self.build_model(input_shape)

    def build_model(self, input_shape: tuple) -> Sequential:
        """
        Builds the LSTM model.

        Args:
            input_shape (tuple): The shape of the input data.

        Returns:
            Sequential: The compiled LSTM model.
        """
        model = Sequential()
        model.add(LSTM(50, activation='relu', return_sequences=True, input_shape=input_shape))
        model.add(Dropout(0.2))
        model.add(LSTM(50, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(1))  # Output layer for regression
        model.compile(optimizer='adam', loss='mean_squared_error')
        return model

    def train(self, data: pd.DataFrame, target_column: str, epochs: int = 50, batch_size: int = 32) -> None:
        """
        Trains the LSTM model on the provided data.

        Args:
            data (pd.DataFrame): The preprocessed data for training.
            target_column (str): The name of the target column for prediction.
            epochs (int): The number of epochs for training.
            batch_size (int): The batch size for training.
        """
        # Prepare the data for LSTM
        X, y = self.prepare_data(data, target_column)
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the model
        self.model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_data=(X_val, y_val))

    def prepare_data(self, data: pd.DataFrame, target_column: str) -> tuple:
        """
        Prepares the data for LSTM training.

        Args:
            data (pd.DataFrame): The preprocessed data.
            target_column (str): The name of the target column for prediction.

        Returns:
            tuple: A tuple containing the features (X) and target (y).
        """
        # Convert DataFrame to numpy array
        values = data.values
        X, y = [], []

        # Create sequences for LSTM
        for i in range(len(values) - 1):
            X.append(values[i:i + 1])  # Use the previous time step as input
            y.append(values[i + 1][data.columns.get_loc(target_column)])  # Target is the next time step

        return np.array(X), np.array(y)

    def evaluate(self, data: pd.DataFrame, target_column: str) -> float:
        """
        Evaluates the model on the provided data.

        Args:
            data (pd.DataFrame): The preprocessed data for evaluation.
            target_column (str): The name of the target column for prediction.

        Returns:
            float: The mean squared error of the model on the evaluation data.
        """
        X, y = self.prepare_data(data, target_column)
        predictions = self.model.predict(X)
        mse = mean_squared_error(y, predictions)
        return mse
