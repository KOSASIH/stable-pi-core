# src/main/arbitration/risk_assessment.py

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import logging

class RiskAssessment:
    def __init__(self, model_path='./models/risk_assessment_model.pkl'):
        self.model_path = model_path
        self.model = None
        logging.info("RiskAssessment initialized with model path: %s", self.model_path)

    def load_data(self, data):
        """
        Load and preprocess the input data for risk assessment.
        
        Args:
            data (dict): A dictionary containing the features for risk assessment.

        Returns:
            pd.DataFrame: Processed features for the model.
        """
        logging.info("Loading data for risk assessment...")
        df = pd.DataFrame(data)
        logging.info("Data loaded with %d samples.", len(df))
        return df

    def train(self, data):
        """
        Train the risk assessment model using the provided data.
        
        Args:
            data (dict): A dictionary containing the features and target variable.
        """
        df = self.load_data(data)

        # Assuming the last column is the target variable (1 for high risk, 0 for low risk)
        X = df.drop(columns=['risk_level'])  # Features
        y = df['risk_level']  # Target variable

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Initialize and train the Random Forest model
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)

        # Evaluate the model
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        logging.info("Model trained successfully with accuracy: %.2f%%", accuracy * 100)
        logging.info("Classification report:\n%s", classification_report(y_test, y_pred))

        # Save the trained model
        self.save_model()

    def assess_risk(self, data):
        """
        Assess the risk based on the input data.
        
        Args:
            data (dict): A dictionary containing the features for risk assessment.

        Returns:
            dict: The risk assessment result indicating the risk level.
        """
        if self.model is None:
            logging.error("Model is not trained. Please train the model before assessment.")
            return None

        # Convert input data to DataFrame
        input_df = pd.DataFrame(data, index=[0])
        prediction = self.model.predict(input_df)
        risk_level = prediction[0]  # 1 for high risk, 0 for low risk

        logging.info("Risk assessment result: %s", "High risk" if risk_level == 1 else "Low risk")
        return {"risk_level": risk_level}

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
