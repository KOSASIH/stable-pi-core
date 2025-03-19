import unittest
from itp.SRC.quantum_entanglement_consensus import QuantumEntanglementConsensus

class TestQuantumEntanglementConsensus(unittest.TestCase):
    def setUp(self):
        """Set up the Quantum Entanglement Consensus for testing."""
        self.qgc = QuantumEntanglementConsensus()
        self.qgc.add_node("Node_A")
        self.qgc.add_node("Node_B")

    def test_propose_transaction(self):
        """Test proposing a transaction."""
        transaction = {'sender': 'PlanetA', 'receiver': 'PlanetB', 'amount': 100}
        self.qgc.propose_transaction(transaction)
        self.assertIn(transaction, self.qgc.transaction_pool)

    def test_reach_consensus(self):
        """Test reaching consensus on a proposed transaction."""
        transaction = {'sender': 'PlanetA', 'receiver': 'PlanetB', 'amount': 100}
        self.qgc.propose_transaction(transaction)
        validated_transactions = self.qgc.reach_consensus()
        self.assertIn(transaction, validated_transactions)

    def test_invalid_transaction(self):
        """Test handling of an invalid transaction."""
        invalid_transaction = {'sender': 'PlanetA', 'receiver': 'PlanetB', 'amount': -50}
        self.qgc.propose_transaction(invalid_transaction)
        validated_transactions = self.qgc.reach_consensus()
        self.assertNotIn(invalid_transaction, validated_transactions)

    def test_multiple_transactions(self):
        """Test proposing and reaching consensus on multiple transactions."""
        transaction1 = {'sender': 'PlanetA', 'receiver': 'PlanetB', 'amount': 100}
        transaction2 = {'sender': 'PlanetC', 'receiver': 'PlanetD', 'amount': 200}
        transaction3 = {'sender': 'PlanetE', 'receiver': 'PlanetF', 'amount': -10}  # Invalid transaction

        self.qgc.propose_transaction(transaction1)
        self.qgc.propose_transaction(transaction2)
        self.qgc.propose_transaction(transaction3)

        validated_transactions = self.qgc.reach_consensus()
        self.assertIn(transaction1, validated_transactions)
        self.assertIn(transaction2, validated_transactions)
        self.assertNotIn(transaction3, validated_transactions)

    def test_consensus_probability(self):
        """Test the probabilistic nature of consensus."""
        transaction = {'sender': 'PlanetA', 'receiver': 'PlanetB', 'amount': 100}
        self.qgc.propose_transaction(transaction)

        # Simulate multiple consensus attempts
        successful_attempts = 0
        for _ in range(100):  # Run multiple attempts
            if self.qgc.simulate_quantum_entanglement(transaction):
                successful_attempts += 1

        # Check that we have some successful attempts
        self.assertGreater(successful_attempts, 0)

if __name__ == "__main__":
    unittest.main()
