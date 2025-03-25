import unittest
from transluminal_reality_weaver import TransluminalRealityWeaver, QuantumState

class TestTransluminalRealityWeaver(unittest.TestCase):

    def setUp(self):
        """Set up a TransluminalRealityWeaver instance for testing."""
        self.trw = TransluminalRealityWeaver()

    def test_create_reality(self):
        """Test the creation of a reality with a specified number of states."""
        states = self.trw.create_reality(5)
        self.assertEqual(len(states), 5)
        self.assertIsInstance(states[0], QuantumState)

    def test_quantum_superposition(self):
        """Test the quantum superposition method."""
        state = self.trw.quantum_superposition()
        self.assertIsInstance(state, QuantumState)
        self.assertIn(state.state_type, ['GTC', 'GU'])
        self.assertGreaterEqual(state.value, 0)
        self.assertLess(state.value, 1)

    def test_simulate_transaction_valid_index(self):
        """Test simulating a transaction with a valid reality index."""
        self.trw.create_reality(3)
        transaction_data = {"transaction_id": 1, "amount": 100}
        try:
            self.trw.simulate_transaction(0, transaction_data)
        except Exception as e:
            self.fail(f"simulate_transaction raised an exception: {e}")

    def test_simulate_transaction_invalid_index(self):
        """Test simulating a transaction with an invalid reality index."""
        transaction_data = {"transaction_id": 1, "amount": 100}
        with self.assertLogs(level='ERROR') as log:
            self.trw.simulate_transaction(0, transaction_data)
            self.assertIn("Reality index out of range. Please provide a valid index.", log.output[0])

    def test_process_transaction(self):
        """Test processing a transaction for a given quantum state."""
        self.trw.create_reality(1)
        state = self.trw.parallel_realities[0][0]
        transaction_data = {"transaction_id": 1, "amount": 100}
        try:
            self.trw.process_transaction(state, transaction_data)
        except Exception as e:
            self.fail(f"process_transaction raised an exception: {e}")

    def test_get_realities(self):
        """Test retrieving the list of created realities."""
        self.trw.create_reality(2)
        realities = self.trw.get_realities()
        self.assertEqual(len(realities), 1)  # Only one reality created
        self.assertEqual(len(realities[0]), 2)  # Two states in that reality

if __name__ == "__main__":
    unittest.main()
