# src/ai/decision_making.py

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib

class DecisionMakingSystem:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False

    def preprocess_data(self, features, labels):
        """
        Preprocess the input data by scaling features and splitting into training and testing sets.
        """
        features_scaled = self.scaler.fit_transform(features)
        X_train, X_test, y_train, y_test = train_test_split(features_scaled, labels, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test

    def train_model(self, features, labels):
        """
        Train the decision-making model using the provided features and labels.
        """
        X_train, X_test, y_train, y_test = self.preprocess_data(features, labels)
        self.model.fit(X_train, y_train)
        self.is_trained = True
        accuracy = self.model.score(X_test, y_test)
        print(f"Model trained with accuracy: {accuracy:.2f}")

    def make_decision(self, input_data):
        """
        Make a decision based on the input data using the trained model.
        """
        if not self.is_trained:
            raise Exception("Model is not trained yet. Please train the model before making decisions.")
        
        input_scaled = self.scaler.transform([input_data])
        prediction = self.model.predict(input_scaled)
        return prediction[0]

    def save_model(self, filename='decision_model.pkl'):
        """
        Save the trained model to a file.
        """
        joblib.dump(self.model, filename)
        joblib.dump(self.scaler, 'scaler.pkl')
        print(f"Model saved to {filename} and scaler saved to scaler.pkl")

    def load_model(self, filename='decision_model.pkl'):
        """
        Load a trained model from a file.
        """
        self.model = joblib.load(filename)
        self.scaler = joblib.load('scaler.pkl')
        self.is_trained = True
        print(f"Model loaded from {filename}")

# Example usage
if __name__ == "__main__":
    # Sample data for training (features and labels)
    features = np.array([[0.1, 0.2], [0.2, 0.3], [0.3, 0.4], [0.4, 0.5], [0.5, 0.6]])
    labels = np.array([0, 0, 1, 1, 1])  # Binary classification

    decision_system = DecisionMakingSystem()
    decision_system.train_model(features, labels)

    # Making a decision based on new input data
    new_data = [0.35, 0.45]
    decision = decision_system.make_decision(new_data)
    print(f"Decision for input {new_data}: {decision}")

    # Save the trained model
    decision_system.save_model()

    # Load the model and make a decision
    loaded_system = DecisionMakingSystem()
    loaded_system.load_model()
    decision = loaded_system.make_decision(new_data)
    print(f"Decision for input {new_data} after loading model: {decision}")
