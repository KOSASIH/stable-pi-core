# src/neuromorphic_analytics/model.py

import numpy as np
import logging

# Set up logging for the Spiking Neural Network Model
logger = logging.getLogger(__name__)

class SpikingNeuralNetworkModel:
    def __init__(self, num_neurons, threshold=1.0, decay=0.9):
        """
        Initialize the Spiking Neural Network Model.

        Parameters:
        - num_neurons (int): Number of neurons in the network.
        - threshold (float): The threshold for neuron firing.
        - decay (float): The decay factor for the neuron's membrane potential.
        """
        self.num_neurons = num_neurons
        self.threshold = threshold
        self.decay = decay
        self.membrane_potential = np.zeros(num_neurons)  # Initialize membrane potential
        logger.info("Spiking Neural Network Model initialized with %d neurons.", num_neurons)

    def predict(self, input_data):
        """
        Make a prediction based on the input data.

        Parameters:
        - input_data (list or np.ndarray): The input data for prediction.

        Returns:
        - list: The output spikes from the network.
        """
        logger.info("Making prediction with input data: %s", input_data)
        input_data = np.array(input_data)
        self.membrane_potential += input_data  # Update membrane potential with input

        # Check for spikes
        spikes = self.membrane_potential >= self.threshold
        self.membrane_potential[spikes] = 0  # Reset potential for neurons that spiked

        # Apply decay to the membrane potential
        self.membrane_potential *= self.decay

        logger.debug("Membrane potential after prediction: %s", self.membrane_potential)
        return spikes.astype(int).tolist()  # Return spikes as a list of 0s and 1s

    def evaluate(self, test_data, true_labels):
        """
        Evaluate the model's performance on test data.

        Parameters:
        - test_data (list of lists or np.ndarray): The data to test the model on.
        - true_labels (list): The true labels for the test data.

        Returns:
        - float: The accuracy of the model on the test data.
        """
        correct_predictions = 0
        total_predictions = len(test_data)

        for data, true_label in zip(test_data, true_labels):
            prediction = self.predict(data)
            if prediction == true_label:
                correct_predictions += 1

        accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0
        logger.info("Model evaluation completed. Accuracy: %.2f", accuracy)
        return accuracy
