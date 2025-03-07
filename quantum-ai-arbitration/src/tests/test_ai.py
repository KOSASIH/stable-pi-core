# tests/test_ai.py

import unittest
from ai.predictive_model import PredictiveModel
from ai.fraud_detection import FraudDetection

class TestPredictiveModel(unittest.TestCase):
    def setUp(self):
        self.model = PredictiveModel(model_path='./models/predictive_model.pkl')

    def test_train_and_predict(self):
        # Mock input data
        data = {
            'feature1': [1, 2, 3, 4],
            'feature2': [4, 5, 6, 7],
            'target': [0, 1, 0, 1]
        }
        self.model.train(data)
        prediction = self.model.predict_outcome({'feature1': 3, 'feature2': 6})
        self.assertIn('predicted_value', prediction)

class TestFraudDetection(unittest.TestCase):
    def setUp(self):
        self.fraud_detector = FraudDetection(model_path='./models/fraud_detection_model.pkl')

    def test_train_and_detect_fraud(self):
        # Mock input data
        data = {
            'feature1': [1, 2, 3, 4],
            'feature2': [4, 5, 6, 7],
            'is_fraud': [0, 1, 0, 1]
        }
        self.fraud_detector.train(data)
        result = self.fraud_detector.detect_fraud({'feature1': 2, 'feature2': 5})
        self.assertIn('is_fraud', result)

if __name__ == '__main__':
    unittest.main()
