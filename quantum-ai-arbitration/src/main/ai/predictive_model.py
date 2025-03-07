# src/main/ai/predictive_model.py

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import logging

class PredictiveModel:
    def __init__(self, model_path='./models/predictive_model.pkl'):
        self.model_path = model_path
        self.model = None
        logging.info("PredictiveModel initialized with model path: %s", self.model_path)

    def load_data(self, data):
        """
        Load and preprocess the input data.
        
        Args:
            data (dict): A dictionary containing the features and target variable.

        Returns:
            tuple: Processed features and target variable.
        """
        logging.info("Loading data for training...")
        df = pd.DataFrame(data)
        X = df.drop(columns=['target'])  # Assuming 'target' is the column to predict
        y = df['target']
        logging.info("Data loaded with %d samples.", len(df))
        return X, y

    def train(self, data):
        """
        Train the predictive model using the provided data.
        
        Args:
            data (dict): A dictionary containing the features and target variable.
        """
        X, y = self.load_data(data)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Initialize and train the model
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        logging.info("Model trained successfully.")

        # Evaluate the model
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        logging.info("Model accuracy: %.2f%%", accuracy * 100)
        logging.info("Classification report:\n%s", classification_report(y_test, y_pred))

        # Save the trained model
        self.save_model()

    def predict_outcome(self, data):
        """
        Predict the outcome based on the input data.
        
        Args:
            data (dict): A dictionary containing the features for prediction.

        Returns:
            dict: The predicted outcome.
        """
        if self.model is None:
            logging.error("Model is not trained. Please train the model before prediction.")
            return None

        # Convert input data to DataFrame
        input_df = pd.DataFrame(data, index=[0])
        prediction = self.model.predict(input_df)
        logging.info("Prediction made: %s", prediction)
        return {"predicted_value": prediction[0]}

    def save_model(self):
        """Save the trained model to a file."""
        joblib.dump(self.model, self.model_path)
        logging.info("Model saved to %s", self.model_path)

    def load_model(self):
        """Load the trained model from a file."""
        try:
            self.model = joblib.load(self.model_path)
            logging.info("Model loaded from %s", self.model_path)
        except FileNotFoundError:
            logging.error("Model file not found. Please train the model first.")
