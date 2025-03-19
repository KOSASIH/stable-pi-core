import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load dataset
def load_data(file_path):
    logging.info("Loading dataset...")
    data = pd.read_csv(file_path)
    logging.info(f"Dataset shape: {data.shape}")
    return data

# Preprocess the data
def preprocess_data(data):
    logging.info("Preprocessing data...")
    # Assuming the last column is the target variable
    X = data.iloc[:, :-1].values
    y = data.iloc[:, -1].values

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standardize the features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    logging.info("Data preprocessing completed.")
    return X_train, X_test, y_train, y_test

# Build the model
def build_model(input_shape):
    logging.info("Building the model...")
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(128, activation='relu', input_shape=(input_shape,)),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')  # Binary classification
    ])

    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    logging.info("Model built successfully.")
    return model

# Train the model
def train_model(model, X_train, y_train, X_test, y_test, epochs=50, batch_size=32):
    logging.info("Training the model...")
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.2)

    # Evaluate the model
    y_pred = (model.predict(X_test) > 0.5).astype("int32")
    logging.info("Model evaluation completed.")
    return y_pred

# Main function
def main():
    # Load and preprocess data
    data = load_data('data/training_data/attack_data.csv')  # Update with your actual data path
    X_train, X_test, y_train, y_test = preprocess_data(data)

    # Build and train the model
    model = build_model(X_train.shape[1])
    y_pred = train_model(model, X_train, y_train, X_test, y_test)

    # Print evaluation metrics
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # Save the model
    model.save('models/attack_detection_model.h5')
    logging.info("Model saved as 'attack_detection_model.h5'.")

if __name__ == "__main__":
    main()
