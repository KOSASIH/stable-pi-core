import pandas as pd
from sklearn.neighbors import NearestNeighbors
import pickle
import os

class RecommendationSystem:
    def __init__(self):
        self.model = NearestNeighbors(n_neighbors=3)

    def train(self, data):
        """Train the recommendation model using user behavior data."""
        features = data[['temperature', 'humidity']]
        self.model.fit(features)

    def recommend(self, new_data):
        """Generate recommendations based on new user data."""
        distances, indices = self.model.kneighbors(new_data)
        return indices

    def save_model(self, filename='models/recommendation_model.pkl'):
        """Save the trained model to a file."""
        with open(filename, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"Model saved to {filename}")

    def load_model(self, filename='models/recommendation_model.pkl'):
        """Load the trained model from a file."""
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                self.model = pickle.load(f)
            print(f"Model loaded from {filename}")
        else:
            print(f"No model found at {filename}")

if __name__ == "__main__":
    # Load user behavior data
    df = pd.read_csv('data/user_behavior.csv')

    # Initialize the recommendation system
    recommender = RecommendationSystem()

    # Train the model
    recommender.train(df)

    # Save the trained model
    recommender.save_model()

    # Example of making a recommendation
    new_user_data = pd.DataFrame({
        'temperature': [22.0],
        'humidity': [60.0]
    })
    recommendations = recommender.recommend(new_user_data)
    print("Recommendations for new user data:", recommendations)
