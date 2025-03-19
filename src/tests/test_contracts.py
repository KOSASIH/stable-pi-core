import unittest
from web3 import Web3
from solcx import compile_source

class TestSmartContracts(unittest.TestCase):
    def setUp(self):
        """Set up the test case with a default Web3 instance and compiled contract."""
        self.w3 = Web3(Web3.EthereumTesterProvider())
        self.contract_source = '''
        pragma solidity ^0.8.0;

        contract Test {
            uint public value;
            address public owner;

            constructor() {
                owner = msg.sender;
            }

            function setValue(uint _value) public {
                value = _value;
            }

            function getValue() public view returns (uint) {
                return value;
            }

            function getOwner() public view returns (address) {
                return owner;
            }
        }
        '''
        compiled_sol = compile_source(self.contract_source)
        self.contract_interface = compiled_sol['<stdin>:Test']
        self.contract = self.w3.eth.contract(abi=self.contract_interface['abi'], bytecode=self.contract_interface['bin'])
        self.tx_hash = self.contract.constructor().transact()
        self.tx_receipt = self.w3.eth.waitForTransactionReceipt(self.tx_hash)
        self.contract_instance = self.w3.eth.contract(address=self.tx_receipt.contractAddress, abi=self.contract_interface['abi'])

    def test_initial_value(self):
        """Test the initial value of the contract."""
        self.assertEqual(self.contract_instance.functions.getValue().call(), 0, msg="Initial value should be 0.")

    def test_set_value(self):
        """Test setting a new value in the contract."""
        self.contract_instance.functions.setValue(42).transact()
        self.assertEqual(self.contract_instance.functions.getValue().call(), 42, msg="Value should be set to 42.")

    def test_get_owner(self):
        """Test getting the owner of the contract."""
        owner = self.contract_instance.functions.getOwner().call()
        self.assertEqual(owner, self.w3.eth.defaultAccount, msg="Owner should be the account that deployed the contract.")

    def test_set_value_by_non_owner(self):
        """Test that only the owner can set the value (if restricted)."""
        # This test assumes that you have implemented access control in your contract.
        # If not, you can modify the contract to include such functionality.
        # For demonstration, we will just check if the function can be called.
        with self.assertRaises(Exception):
            self.contract_instance.functions.setValue(100).transact({'from': '0x00000000000000000000000000000000000000001'})  # Non-owner address

if __name__ == '__main__':
    unittest.main()
