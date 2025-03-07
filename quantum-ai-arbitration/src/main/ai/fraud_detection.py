# src/main/ai/fraud_detection.py

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import logging

class FraudDetection:
    def __init__(self, model_path='./models/fraud_detection_model.pkl'):
        self.model_path = model_path
        self.model = None
        logging.info("FraudDetection initialized with model path: %s", self.model_path)

    def load_data(self, data):
        """
        Load and preprocess the input data for fraud detection.
        
        Args:
            data (dict): A dictionary containing the features for fraud detection.

        Returns:
            pd.DataFrame: Processed features for the model.
        """
        logging.info("Loading data for fraud detection...")
        df = pd.DataFrame(data)
        logging.info("Data loaded with %d samples.", len(df))
        return df

    def train(self, data):
        """
        Train the fraud detection model using the provided data.
        
        Args:
            data (dict): A dictionary containing the features for fraud detection.
        """
        df = self.load_data(data)

        # Assuming the last column is the target variable (1 for fraud, 0 for non-fraud)
        X = df.drop(columns=['is_fraud'])  # Features
        y = df['is_fraud']  # Target variable

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Initialize and train the Isolation Forest model
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.model.fit(X_train)

        # Evaluate the model
        y_pred = self.model.predict(X_test)
        y_pred = [1 if x == -1 else 0 for x in y_pred]  # Convert to binary (1 for fraud, 0 for non-fraud)

        logging.info("Model trained successfully.")
        logging.info("Confusion Matrix:\n%s", confusion_matrix(y_test, y_pred))
        logging.info("Classification Report:\n%s", classification_report(y_test, y_pred))

        # Save the trained model
        self.save_model()

    def detect_fraud(self, data):
        """
        Detect fraud based on the input data.
        
        Args:
            data (dict): A dictionary containing the features for fraud detection.

        Returns:
            dict: The detection result indicating whether fraud is detected.
        """
        if self.model is None:
            logging.error("Model is not trained. Please train the model before detection.")
            return None

        # Convert input data to DataFrame
        input_df = pd.DataFrame(data, index=[0])
        prediction = self.model.predict(input_df)
        is_fraud = 1 if prediction[0] == -1 else 0  # -1 indicates anomaly (fraud)

        logging.info("Fraud detection result: %s", "Fraud detected" if is_fraud else "No fraud detected")
        return {"is_fraud": is_fraud}

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
