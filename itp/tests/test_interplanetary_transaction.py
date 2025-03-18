import unittest
from itp.SRC.interplanetary_transaction_protocol import InterplanetaryTransactionProtocol
from itp.SRC.space_time_synchronization import SpaceTimeSynchronization
from itp.SRC.quantum_entanglement_consensus import QuantumEntanglementConsensus

class TestInterplanetaryTransactionProtocol(unittest.TestCase):
    def setUp(self):
        """Set up the Interplanetary Transaction Protocol for testing."""
        self.itp = InterplanetaryTransactionProtocol()
        self.stsp = SpaceTimeSynchronization()
        self.qgc = QuantumEntanglementConsensus()

    def test_create_transaction(self):
        """Test creating a transaction."""
        transaction = self.itp.create_transaction("PlanetA", "PlanetB", 100)
        self.assertEqual(transaction['sender'], "PlanetA")
        self.assertEqual(transaction['receiver'], "PlanetB")
        self.assertEqual(transaction['amount'], 100)
        self.assertEqual(transaction['status'], 'pending')

    def test_validate_transaction(self):
        """Test validating a transaction."""
        valid_transaction = {'sender': 'PlanetA', 'receiver': 'PlanetB', 'amount': 100, 'status': 'pending'}
        invalid_transaction = {'sender': 'PlanetA', 'receiver': 'PlanetB', 'amount': -50, 'status': 'pending'}
        
        self.assertTrue(self.itp.validate_transaction(valid_transaction))
        self.assertFalse(self.itp.validate_transaction(invalid_transaction))

    def test_execute_transaction(self):
        """Test executing a valid transaction."""
        transaction = self.itp.create_transaction("PlanetA", "PlanetB", 100)
        self.itp.execute_transaction(transaction)
        self.assertEqual(transaction['status'], 'executed')

    def test_execute_invalid_transaction(self):
        """Test executing an invalid transaction."""
        transaction = self.itp.create_transaction("PlanetA", "PlanetB", -100)
        self.itp.execute_transaction(transaction)
        self.assertEqual(transaction['status'], 'pending')  # Should remain pending due to validation failure

    def test_timestamp_transaction(self):
        """Test timestamping a transaction."""
        self.stsp.synchronize_time(time.time() + 5)  # Simulate synchronization
        transaction = self.itp.create_transaction("PlanetA", "PlanetB", 100)
        timestamp = self.itp.timestamp_transaction()
        self.assertAlmostEqual(timestamp, self.stsp.get_current_time(), delta=1)

    def test_process_transactions(self):
        """Test processing multiple transactions."""
        self.itp.create_transaction("PlanetA", "PlanetB", 100)
        self.itp.create_transaction("PlanetC", "PlanetD", 200)
        self.itp.process_transactions()
        for transaction in self.itp.transactions:
            self.assertEqual(transaction['status'], 'executed')

    def test_consensus_integration(self):
        """Test integration with Quantum Entanglement Consensus."""
        self.qgc.add_node("Node_A")
        self.qgc.add_node("Node_B")
        transaction = {'sender': 'PlanetA', 'receiver': 'PlanetB', 'amount': 100}
        self.qgc.propose_transaction(transaction)
        validated_transactions = self.qgc.reach_consensus()
        self.assertIn(transaction, validated_transactions)

if __name__ == "__main__":
    unittest.main()
