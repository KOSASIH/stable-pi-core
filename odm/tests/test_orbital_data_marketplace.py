# tests/test_orbital_data_marketplace.py

import unittest
from web3 import Web3
from odm.contracts.orbital_data_marketplace import OrbitalDataMarketplace  # Assuming you have a smart contract class

class TestOrbitalDataMarketplace(unittest.TestCase):

    def setUp(self):
        """Set up the Web3 connection and contract instance."""
        self.w3 = Web3(Web3.EthereumTesterProvider())
        self.contract = OrbitalDataMarketplace.deploy({'from': self.w3.eth.accounts[0]})

    def test_contract_initialization(self):
        """Test if the contract initializes correctly."""
        self.assertIsNotNone(self.contract)

    def test_add_listing(self):
        """Test adding a data listing to the marketplace."""
        tx_hash = self.contract.addListing("Test Data", "This is a test.", {'from': self.w3.eth.accounts[0]})
        self.w3.eth.waitForTransactionReceipt(tx_hash)
        listing = self.contract.getListing(0)
        self.assertEqual(listing[0], "Test Data")
        self.assertEqual(listing[1], "This is a test.")

    def test_remove_listing(self):
        """Test removing a data listing from the marketplace."""
        self.contract.addListing("Test Data", "This is a test.", {'from': self.w3.eth.accounts[0]})
        tx_hash = self.contract.removeListing(0, {'from': self.w3.eth.accounts[0]})
        self.w3.eth.waitForTransactionReceipt(tx_hash)
        with self.assertRaises(Exception):
            self.contract.getListing(0)

if __name__ == '__main__':
    unittest.main()
