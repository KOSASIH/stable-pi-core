# hqag.test.py

import unittest
from hqag import HyperQuantumAIGovernance

class TestHyperQuantumAIGovernance(unittest.TestCase):
    def setUp(self):
        """Set up a new HyperQuantumAIGovernance instance for testing."""
        self.hqag = HyperQuantumAIGovernance()

    def test_make_decision_success(self):
        """Test successful decision making."""
        self.hqag.make_decision("Implement new AI ethics guidelines.")
        self.assertEqual(len(self.hqag.decisions), 1)
        self.assertEqual(self.hqag.decisions[0], "Implement new AI ethics guidelines.")
        self.assertEqual(len(self.hqag.decision_log), 1)
        self.assertEqual(self.hqag.decision_log[0]['decision'], "Implement new AI ethics guidelines.")
        self.assertEqual(self.hqag.decision_log[0]['impact'], "Positive")

    def test_make_decision_with_stakeholders(self):
        """Test decision making with stakeholders and consensus."""
        self.hqag.make_decision("Increase funding for research.", stakeholders=["Stakeholder_1", "Stakeholder_2"])
        self.assertEqual(len(self.hqag.decisions), 1)
        self.assertEqual(self.hqag.decisions[0], "Increase funding for research.")

    def test_make_decision_without_consensus(self):
        """Test decision making without reaching consensus."""
        with self.assertRaises(ValueError) as context:
            self.hqag.make_decision("Reduce funding for non-essential projects.", stakeholders=["Stakeholder_1", "Stakeholder_2"])
        self.assertEqual(str(context.exception), "Consensus not reached among stakeholders.")

    def test_analyze_decision_positive(self):
        """Test analysis of a positive decision."""
        impact = self.hqag.analyze_decision("This decision will benefit the community.")
        self.assertEqual(impact, "Positive")

    def test_analyze_decision_negative(self):
        """Test analysis of a negative decision."""
        impact = self.hqag.analyze_decision("This decision will harm the environment.")
        self.assertEqual(impact, "Negative")

    def test_get_decision_history(self):
        """Test retrieval of decision history."""
        self.hqag.make_decision("Implement new AI ethics guidelines.")
        self.hqag.make_decision("Increase funding for research.")
        history = self.hqag.get_decision_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]['decision'], "Implement new AI ethics guidelines.")
        self.assertEqual(history[1]['decision'], "Increase funding for research.")

if __name__ == "__main__":
    unittest.main()
