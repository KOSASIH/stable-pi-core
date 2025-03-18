import unittest
from core.config import Config
from itp.SRC.transaction_manager import TransactionManager
from itp.SRC.space_time_synchronization import SpaceTimeSynchronization
from itp.SRC.quantum_entanglement_consensus import QuantumEntanglementConsensus

class TestTransactionManager(unittest.TestCase):
    def setUp(self):
        """Set up the Transaction Manager for testing."""
        self.tm = TransactionManager()

    def test_create_transaction(self):
        """Test creating a transaction."""
        transaction = self.tm.create_transaction("PlanetA", "PlanetB", 100)
        self.assertEqual(transaction['sender'], "PlanetA")
        self.assertEqual(transaction['receiver'], "PlanetB")
        self.assertEqual(transaction['amount'], 100)
        self.assertEqual(transaction['status'], 'pending')

    def test_validate_transaction(self):
        """Test validating a transaction."""
        valid_transaction = {'sender': 'PlanetA', 'receiver': 'PlanetB', 'amount': 100, 'status': 'pending'}
        invalid_transaction = {'sender': 'PlanetA', 'receiver': 'PlanetB', 'amount': -50, 'status': 'pending'}
        
        self.assertTrue(self.tm.validate_transaction(valid_transaction))
        self.assertFalse(self.tm.validate_transaction(invalid_transaction))

    def test_execute_transaction(self):
        """Test executing a valid transaction."""
        transaction = self.tm.create_transaction("PlanetA", "PlanetB", 100)
        self.tm.execute_transaction(transaction)
        self.assertEqual(transaction['status'], 'executed')

    def test_execute_invalid_transaction(self):
        """Test executing an invalid transaction."""
        transaction = self.tm.create_transaction("PlanetA", "PlanetB", -100)
        self.tm.execute_transaction(transaction)
        self.assertEqual(transaction['status'], 'pending')  # Should remain pending due to validation failure

class TestSpaceTimeSynchronization(unittest.TestCase):
    def setUp(self):
        """Set up the Space-Time Synchronization for testing."""
        self.stsp = SpaceTimeSynchronization()

    def test_synchronize_time(self):
        """Test synchronizing time with a celestial body."""
        celestial_time = 1633072800  # Example celestial body time
        self.stsp.synchronize_time(celestial_time)
        self.assertAlmostEqual(self.stsp.local_time_offset, celestial_time - time.time(), delta=1)

    def test_get_current_time(self):
        """Test getting the current synchronized time."""
        self.stsp.synchronize_time(time.time() + 5)  # Simulate synchronization
        current_time = self.stsp.get_current_time()
        self.assertAlmostEqual(current_time, time.time() + 5, delta=1)

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

if __name__ == "__main__":
    unittest.main()
