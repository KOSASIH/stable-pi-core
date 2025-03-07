# tests/test_arbitration.py

import unittest
from arbitration.arbitration_service import ArbitrationService
from quantum.quantum_solver import QuantumSolver
from ai.predictive_model import PredictiveModel
from ai.fraud_detection import FraudDetection
from arbitration.risk_assessment import RiskAssessment

class TestArbitrationService(unittest.TestCase):
    def setUp(self):
        self.quantum_solver = QuantumSolver()
        self.predictive_model = PredictiveModel()
        self.fraud_detection = FraudDetection()
        self.risk_assessment = RiskAssessment()
        self.arbitration_service = ArbitrationService(
            self.quantum_solver,
            self.predictive_model,
            self.fraud_detection,
            self.risk_assessment
        )

    def test_process_arbitration(self):
        raw_data = {
            "historical_data": [100, 200, 300],
            "transaction_data": {"amount": 150, "currency": "USD"},
            "is_fraud": 0,
            "risk_level": 0
        }
        results = self.arbitration_service.process_arbitration(raw_data)
        self.assertIn('risk_assessment', results)
        self.assertIn('fraud_detection', results)
        self.assertIn('optimization', results)
        self.assertIn('prediction', results)

if __name__ == '__main__':
    unittest.main()
