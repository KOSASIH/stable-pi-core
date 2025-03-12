import unittest
from stabilization import AdvancedStabilizationAlgorithm

class TestStabilization(unittest.TestCase):
    def setUp(self):
        """Set up the test case with a default stabilizer instance."""
        self.stabilizer = AdvancedStabilizationAlgorithm(target_value=100, adjustment_factor=0.1, smoothing_factor=0.5)

    def test_adjust_value_below_target(self):
        """Test adjusting a value below the target."""
        adjusted_value = self.stabilizer.adjust_value(90)
        self.assertAlmostEqual(adjusted_value, 95.0, places=1, msg="Adjusted value should be closer to the target.")

    def test_adjust_value_above_target(self):
        """Test adjusting a value above the target."""
        adjusted_value = self.stabilizer.adjust_value(110)
        self.assertAlmostEqual(adjusted_value, 105.0, places=1, msg="Adjusted value should be closer to the target.")

    def test_get_current_value_initial(self):
        """Test getting the current value before any adjustments."""
        self.assertEqual(self.stabilizer.get_current_value(), 100.0, msg="Initial value should be equal to the target value.")

    def test_get_current_value_after_adjustment(self):
        """Test getting the current value after an adjustment."""
        self.stabilizer.adjust_value(90)
        self.assertEqual(self.stabilizer.get_current_value(), 95.0, msg="Current value should reflect the adjustment.")

    def test_reset(self):
        """Test resetting the stabilizer to the target value."""
        self.stabilizer.adjust_value(90)
        self.stabilizer.reset()
        self.assertEqual(self.stabilizer.get_current_value(), 100.0, msg="Reset value should be equal to the target value.")

    def test_adjust_value_with_invalid_input(self):
        """Test adjusting with an invalid input."""
        with self.assertRaises(TypeError):
            self.stabilizer.adjust_value("invalid")

    def test_smoothing_effect(self):
        """Test the smoothing effect over multiple adjustments."""
        self.stabilizer.adjust_value(90)  # First adjustment
        self.stabilizer.adjust_value(95)   # Second adjustment
        self.assertAlmostEqual(self.stabilizer.get_current_value(), 97.5, places=1, msg="Smoothing effect should be applied.")

if __name__ == '__main__':
    unittest.main()
