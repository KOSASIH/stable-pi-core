import json
from flask import Flask, render_template, request, jsonify
from typing import List, Dict, Any
from .predictions import generate_recommendations
from .model import PredictiveModel

class GovernanceDashboard:
    """
    A class to create a Community-Driven Governance Dashboard.

    Attributes:
        app (Flask): The Flask application instance.
        model (PredictiveModel): The trained predictive model.
    """

    def __init__(self, model: PredictiveModel):
        self.app = Flask(__name__)
        self.model = model
        self.setup_routes()

    def setup_routes(self):
        """Sets up the routes for the Flask application."""
        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.app.route('/recommendations', methods=['POST'])
        def recommendations():
            data = request.json
            target_column = data.get('target_column')
            num_recommendations = data.get('num_recommendations', 5)
            predictions_data = data.get('predictions_data')

            if not predictions_data or not target_column:
                return jsonify({"error": "Invalid input data"}), 400

            # Generate recommendations
            recommendations = generate_recommendations(self.model, predictions_data, target_column, num_recommendations)
            return jsonify(recommendations)

    def run(self, host: str = '0.0.0.0', port: int = 5000):
        """Runs the Flask application."""
        self.app.run(host=host, port=port)

# Example usage
if __name__ == "__main__":
    # Load or create your predictive model here
    model = PredictiveModel(input_shape=(1, 10))  # Example input shape
    model.train(data, target_column='target')  # Replace with actual training data

    dashboard = GovernanceDashboard(model)
    dashboard.run()
