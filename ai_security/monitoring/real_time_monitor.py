import pandas as pd
import numpy as np
import tensorflow as tf
import logging
import time
import random

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load the trained model
def load_model(model_path):
    logging.info("Loading the model...")
    model = tf.keras.models.load_model(model_path)
    logging.info("Model loaded successfully.")
    return model

# Simulate real-time data stream
def generate_fake_data():
    # Simulate a random transaction or event
    return {
        'amount': random.randint(1, 5000),
        'time_of_day': random.choice(['08:00', '12:00', '15:00', '20:00']),
        'location': random.choice(['New York', 'Los Angeles', 'Chicago']),
        'is_fraud': random.choice([0, 1])  # Randomly assign fraud label for simulation
    }

# Monitor incoming data
def monitor_data(model):
    logging.info("Starting real-time monitoring...")
    while True:
        # Simulate receiving new data
        new_data = generate_fake_data()
        logging.info(f"New data received: {new_data}")

        # Prepare data for prediction
        input_data = np.array([[new_data['amount'], new_data['time_of_day'], new_data['location']]])
        # Note: You may need to preprocess the input data as per your model's requirements

        # Make prediction
        prediction = model.predict(input_data)
        is_fraud = (prediction > 0.5).astype("int32")[0][0]

        if is_fraud:
            logging.warning("Fraudulent activity detected!")
            # Trigger alert
            trigger_alert(new_data)

        time.sleep(5)  # Simulate a delay for the next data point

# Trigger an alert
def trigger_alert(data):
    logging.info(f"Alert triggered for data: {data}")

# Main function
def main():
    model_path = 'models/fraud_detection_model.h5'  # Update with your model path
    model = load_model(model_path)
    monitor_data(model)

if __name__ == "__main__":
    main()
