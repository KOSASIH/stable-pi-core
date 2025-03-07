import unittest
from pegging_algorithm import PeggingMechanism

class TestPeggingMechanism(unittest.TestCase):
    def setUp(self):
        self.pegging_mechanism = PeggingMechanism(target_price=314159.00, adjustment_factor=0.01)

    def test_initial_supply(self):
        self.assertEqual(self.pegging_mechanism.current_supply, 1000000)

    def test_adjust_supply_increase(self):
        # Simulate a price increase
        self.pegging_mechanism.get_current_price = lambda: 320.0  # Simulate price above target
        initial_supply = self.pegging_mechanism.current_supply
        self.pegging_mechanism.adjust_supply()
        self.assertGreater(self.pegging_mechanism.current_supply, initial_supply)

    def test_adjust_supply_decrease(self):
        # Simulate a price decrease
        self.pegging_mechanism.get_current_price = lambda: 310.0  # Simulate price below target
        initial_supply = self.pegging_mechanism.current_supply
        self.pegging_mechanism.adjust_supply()
        self.assertLess(self.pegging_mechanism.current_supply, initial_supply)

    def test_no_adjustment_within_threshold(self):
        # Simulate a price within the threshold
        self.pegging_mechanism.get_current_price = lambda: 313.0  # Simulate price close to target
        initial_supply = self.pegging_mechanism.current_supply
        self.pegging_mechanism.adjust_supply()
        self.assertEqual(self.pegging_mechanism.current_supply, initial_supply)

if __name__ == "__main__":
    unittest.main()
