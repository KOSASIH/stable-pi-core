# tests/test_pqpn.py

import unittest
import numpy as np
from pqpn.photonic_processor import PhotonicProcessor
from pqpn.data_transmission import PhotonicDataTransmission
from pqpn.quantum_ai import QuantumAI

class TestPhotonicProcessor(unittest.TestCase):
    def setUp(self):
        """Set up a PhotonicProcessor instance for testing."""
        self.processor = PhotonicProcessor(processor_type="PsiQuantum", id=1)
        self.processor.add_qubit()  # Add a qubit for testing

    def test_add_qubit(self):
        """Test adding a qubit to the processor."""
        initial_count = len(self.processor.qubits)
        self.processor.add_qubit()
        self.assertEqual(len(self.processor.qubits), initial_count + 1)

    def test_apply_gate_to_qubit(self):
        """Test applying a gate to a qubit."""
        hadamard_gate = np.array([[1/np.sqrt(2), 1/np.sqrt(2)],
                                   [1/np.sqrt(2), -1/np.sqrt(2)]])
        self.processor.apply_gate_to_qubit(0, hadamard_gate)
        self.assertIsNotNone(self.processor.qubits[0].state)

    def test_measure_qubit(self):
        """Test measuring a qubit."""
        result = self.processor.measure_qubit(0)
        self.assertIn(result, [0, 1])

class TestPhotonicDataTransmission(unittest.TestCase):
    def setUp(self):
        """Set up a PhotonicDataTransmission instance for testing."""
        self.config = {
            'transmission_layer': 'Photonic',
            'max_bandwidth': 10.0,
            'latency': 0.05,
            'error_correction': {
                'enabled': True,
                'packet_loss_rate': 0.05
            }
        }
        self.data_transmission = PhotonicDataTransmission(self.config)

    def test_send_data(self):
        """Test sending data."""
        result = self.data_transmission.send_data("Test Data", "Node_1")
        self.assertTrue(result)

    def test_receive_data(self):
        """Test receiving data."""
        with self.assertLogs(logger, level='INFO') as log:
            self.data_transmission.receive_data("Test Data")
            self.assertIn("Data received successfully: Test Data", log.output[-1])

class TestQuantumAI(unittest.TestCase):
    def setUp(self):
        """Set up a QuantumAI instance for testing."""
        self.config = {
            'algorithm': 'Quantum-AI-Arbitration',
            'model_parameters': {
                'learning_rate': 0.01,
                'n_iterations': 100
            }
        }
        self.quantum_ai = QuantumAI(self.config)
        self.X, self.y = self.quantum_ai.generate_synthetic_data(n_samples=100, n_features=4, n_classes=2)
        self.X_train, self.X_test, self.y_train, self.y_test = self.quantum_ai.train_test_split(self.X, self.y)

    def test_train_model(self):
        """Test training the Quantum AI model."""
        self.quantum_ai.train_model(self.X_train, self.y_train)
        self.assertIsNotNone(self.quantum_ai.model)

    def test_predict(self):
        """Test making predictions with the trained model."""
        self.quantum_ai.train_model(self.X_train, self.y_train)
        predictions = self.quantum_ai.predict(self.X_test)
        self.assertEqual(len(predictions), len(self.X_test))

    def test_evaluate_model(self):
        """Test evaluating the Quantum AI model."""
        self.quantum_ai.train_model(self.X_train, self.y_train)
        accuracy = self.quantum_ai.evaluate_model(self.X_test, self.y_test)
        self.assertIsNotNone(accuracy)

if __name__ == "__main__":
    unittest.main()
