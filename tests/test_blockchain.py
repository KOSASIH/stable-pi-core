import unittest
from unittest.mock import patch
from blockchain import Blockchain
from transaction import Transaction

class TestBlockchain(unittest.TestCase):
    def setUp(self):
        """Set up a new blockchain for testing."""
        self.blockchain = Blockchain()

    def test_create_block(self):
        """Test creating a new block."""
        previous_hash = self.blockchain.get_last_block()['hash']
        new_block = self.blockchain.create_block(previous_hash)
        self.assertEqual(new_block['index'], 1)
        self.assertEqual(new_block['previous_hash'], previous_hash)
        self.assertEqual(len(new_block['transactions']), 0)  # No transactions yet

    def test_add_transaction(self):
        """Test adding a valid transaction to the blockchain."""
        transaction = Transaction(sender="Alice", recipient="Bob", amount=50)
        self.blockchain.add_transaction(transaction)
        self.assertEqual(len(self.blockchain.current_transactions), 1)

    def test_add_invalid_transaction(self):
        """Test adding an invalid transaction."""
        with self.assertRaises(ValueError):
            self.blockchain.add_transaction(Transaction(sender="Alice", recipient="Bob", amount=-50))

    def test_mine_block(self):
        """Test mining a block with valid transactions."""
        self.blockchain.add_transaction(Transaction(sender="Alice", recipient="Bob", amount=50))
        previous_hash = self.blockchain.get_last_block()['hash']
        mined_block = self.blockchain.mine_block(previous_hash)
        self.assertEqual(mined_block['previous_hash'], previous_hash)
        self.assertEqual(len(mined_block['transactions']), 1)

    def test_mine_block_without_transactions(self):
        """Test mining a block without any transactions."""
        previous_hash = self.blockchain.get_last_block()['hash']
        mined_block = self.blockchain.mine_block(previous_hash)
        self.assertEqual(mined_block['previous_hash'], previous_hash)
        self.assertEqual(len(mined_block['transactions']), 0)  # Should be empty

    def test_chain_validation(self):
        """Test validating the blockchain."""
        self.blockchain.add_transaction(Transaction(sender="Alice", recipient="Bob", amount=50))
        previous_hash = self.blockchain.get_last_block()['hash']
        self.blockchain.mine_block(previous_hash)
        self.assertTrue(self.blockchain.is_chain_valid())

    def test_invalid_chain(self):
        """Test chain validation with tampered data."""
        self.blockchain.add_transaction(Transaction(sender="Alice", recipient="Bob", amount=50))
        previous_hash = self.blockchain.get_last_block()['hash']
        self.blockchain.mine_block(previous_hash)

        # Tamper with the blockchain
        self.blockchain.chain[1]['transactions'][0]['amount'] = 1000
        self.assertFalse(self.blockchain.is_chain_valid())

    @patch('time.sleep', return_value=None)  # Mock sleep to speed up tests
    def test_performance_mining(self, mock_sleep):
        """Test performance of mining under load."""
        for i in range(100):
            self.blockchain.add_transaction(Transaction(sender="Alice", recipient="Bob", amount=50))
        previous_hash = self.blockchain.get_last_block()['hash']
        mined_block = self.blockchain.mine_block(previous_hash)
        self.assertEqual(len(mined_block['transactions']), 100)

if __name__ == '__main__':
    unittest.main()
