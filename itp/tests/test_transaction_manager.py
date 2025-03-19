import unittest
from itp.SRC.transaction_manager import TransactionManager

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

    def test_execute_transaction_with_contract(self):
        """Test executing a transaction with a smart contract."""
        def mock_contract(transaction):
            """Mock smart contract function."""
            return True  # Simulate successful contract execution

        transaction = self.tm.create_transaction("PlanetA", "PlanetB", 100, contract=mock_contract)
        self.tm.execute_transaction(transaction)
        self.assertEqual(transaction['status'], 'executed')  # Contract execution should succeed

    def test_get_all_transactions(self):
        """Test retrieving all transactions."""
        self.tm.create_transaction("PlanetA", "PlanetB", 100)
        self.tm.create_transaction("PlanetC", "PlanetD", 200)
        transactions = self.tm.get_all_transactions()
        self.assertEqual(len(transactions), 2)  # Should return 2 transactions

    def test_get_executed_transactions(self):
        """Test retrieving executed transactions."""
        transaction1 = self.tm.create_transaction("PlanetA", "PlanetB", 100)
        transaction2 = self.tm.create_transaction("PlanetC", "PlanetD", 200)
        self.tm.execute_transaction(transaction1)  # Execute first transaction
        executed_transactions = self.tm.get_executed_transactions()
        self.assertIn(transaction1, executed_transactions)
        self.assertNotIn(transaction2, executed_transactions)  # Second transaction not executed yet

if __name__ == "__main__":
    unittest.main()
