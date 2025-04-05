# cere.test.py

import unittest
from cere import CosmicEntropyReversalEngine

class TestCosmicEntropyReversalEngine(unittest.TestCase):
    def setUp(self):
        """Set up a new CosmicEntropyReversalEngine instance for testing."""
        self.cere = CosmicEntropyReversalEngine()

    def test_monitor_entropy_success(self):
        """Test successful monitoring of entropy level."""
        self.cere.monitor_entropy("Node_A", 5)
        self.assertIn("Node_A", self.cere.entropy_levels)
        self.assertEqual(self.cere.entropy_levels["Node_A"], 5)

    def test_log_entropy_success(self):
        """Test successful logging of entropy level."""
        self.cere.monitor_entropy("Node_A", 5)
        log_entry = self.cere.get_entropy_log()[-1]
        self.assertEqual(log_entry['node_id'], "Node_A")
        self.assertEqual(log_entry['level'], 5)

    def test_reverse_entropy_success(self):
        """Test successful reversal of entropy level."""
        self.cere.monitor_entropy("Node_A", 5)
        self.cere.reverse_entropy("Node_A")
        self.assertEqual(self.cere.entropy_levels["Node_A"], 4)

    def test_reverse_entropy_not_monitored(self):
        """Test reversal of entropy for a node that is not monitored."""
        with self.assertRaises(ValueError) as context:
            self.cere.reverse_entropy("Node_B")
        self.assertEqual(str(context.exception), "Node Node_B is not being monitored.")

    def test_reverse_entropy_already_minimum(self):
        """Test reversal of entropy when already at minimum level."""
        self.cere.monitor_entropy("Node_A", 0)
        self.cere.reverse_entropy("Node_A")
        self.assertEqual(self.cere.entropy_levels["Node_A"], 0)  # Should remain at 0

    def test_get_entropy_levels(self):
        """Test retrieval of current entropy levels."""
        self.cere.monitor_entropy("Node_A", 5)
        self.cere.monitor_entropy("Node_B", 3)
        levels = self.cere.get_entropy_levels()
        self.assertEqual(levels["Node_A"], 5)
        self.assertEqual(levels["Node_B"], 3)

    def test_get_entropy_log(self):
        """Test retrieval of entropy log."""
        self.cere.monitor_entropy("Node_A", 5)
        self.cere.reverse_entropy("Node_A")
        log = self.cere.get_entropy_log()
        self.assertEqual(len(log), 2)  # One for monitoring, one for reversal
        self.assertEqual(log[0]['node_id'], "Node_A")
        self.assertEqual(log[1]['node_id'], "Node_A")
        self.assertEqual(log[1]['old_level'], 5)
        self.assertEqual(log[1]['new_level'], 4)

if __name__ == "__main__":
    unittest.main()
