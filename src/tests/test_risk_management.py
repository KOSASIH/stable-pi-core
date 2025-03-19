import unittest
from risk_management import RiskManagementSystem

class TestRiskManagement(unittest.TestCase):
    def setUp(self):
        """Set up the test case with a default risk management system instance."""
        self.risk_manager = RiskManagementSystem()

    def test_add_risk(self):
        """Test adding a risk to the system."""
        self.risk_manager.add_risk(1, "Market volatility", 0.7, 0.9, "Diversify portfolio")
        self.assertEqual(len(self.risk_manager.risks), 1, msg="Risk should be added to the system.")
        self.assertEqual(self.risk_manager.risks[1]['description'], "Market volatility", msg="Risk description should match.")

    def test_mitigate_risk(self):
        """Test mitigating a risk."""
        self.risk_manager.add_risk(1, "Market volatility", 0.7, 0.9, "Diversify portfolio")
        mitigation_message = self.risk_manager.mitigate_risk(1)
        self.assertIn("Diversify portfolio", mitigation_message, msg="Mitigation message should contain the strategy.")

    def test_monitor_risks(self):
        """Test monitoring risks."""
        self.risk_manager.add_risk(1, "Market volatility", 0.7, 0.9, "Diversify portfolio")
        risks_report = self.risk_manager.monitor_risks()
        self.assertIn("Market volatility", risks_report, msg="Risk report should include the added risk.")

    def test_remove_risk(self):
        """Test removing a risk from the system."""
        self.risk_manager.add_risk(1, "Market volatility", 0.7, 0.9, "Diversify portfolio")
        self.risk_manager.remove_risk(1)
        self.assertEqual(len(self.risk_manager.risks), 0, msg="Risk should be removed from the system.")

    def test_add_risk_with_invalid_data(self):
        """Test adding a risk with invalid data."""
        with self.assertRaises(ValueError):
            self.risk_manager.add_risk(2, "", 0.7, 0.9, "Diversify portfolio")  # Invalid description

    def test_mitigate_nonexistent_risk(self):
        """Test mitigating a risk that does not exist."""
        with self.assertRaises(KeyError):
            self.risk_manager.mitigate_risk(999)  # Nonexistent risk ID

    def test_monitor_empty_risks(self):
        """Test monitoring when there are no risks."""
        risks_report = self.risk_manager.monitor_risks()
        self.assertEqual(risks_report, "No risks to report.", msg="Should indicate no risks are present.")

if __name__ == '__main__':
    unittest.main()
