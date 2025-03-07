# src/api.py

from flask import Flask, request, jsonify
from utils import load_model, preprocess_input, validate_input
import logging

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the trained model
model_path = 'models/price_prediction_model.pkl'
try:
    model = load_model(model_path)
except Exception as e:
    logging.critical(f"Failed to load model: {e}")
    exit(1)  # Exit if the model cannot be loaded

@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint to make predictions."""
    data = request.get_json()  # Get JSON data from the request

    # Validate input data
    if 'input' not in data:
        logging.warning("No input data provided.")
        return jsonify({'error': 'No input data provided'}), 400

    input_data = data['input']
    
    try:
        validate_input(input_data)  # Validate the input format
        preprocessed_input = preprocess_input(input_data)  # Preprocess the input data

        # Make prediction
        prediction = model.predict(preprocessed_input)

        logging.info(f"Prediction made successfully: {prediction[0]}")
        return jsonify({'predicted_price': prediction[0].tolist()})
    
    except ValueError as ve:
        logging.warning(f"Input validation error: {ve}")
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        return jsonify({'error': 'An error occurred during prediction'}), 500

if __name__ == '__main__':
    app.run(debug=True)
