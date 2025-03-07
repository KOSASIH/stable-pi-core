import unittest
from web3 import Web3
from solcx import compile_source

class TestStabilizationContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Connect to a local Ethereum node (e.g., Ganache)
        cls.w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
        cls.account = cls.w3.eth.accounts[0]

        # Compile the smart contract
        contract_source = '''
        pragma solidity ^0.8.0;

        contract Stabilization {
            uint256 public pegValue;
            uint256 public currentSupply;

            constructor(uint256 _pegValue) {
                pegValue = _pegValue;
                currentSupply = 0;
            }

            function adjustSupply(uint256 newSupply) public {
                currentSupply = newSupply;
            }
        }
        '''
        compiled_sol = compile_source(contract_source)
        cls.contract_interface = compiled_sol['<stdin>:Stabilization']
        cls.contract = cls.w3.eth.contract(abi=cls.contract_interface['abi'], bytecode=cls.contract_interface['bin'])

        # Deploy the contract
        tx_hash = cls.contract.constructor(314159).transact({'from': cls.account})
        tx_receipt = cls.w3.eth.waitForTransactionReceipt(tx_hash)
        cls.contract_instance = cls.w3.eth.contract(address=tx_receipt.contractAddress, abi=cls.contract_interface['abi'])

    def test_initial_values(self):
        self.assertEqual(self.contract_instance.functions.pegValue().call(), 314159)
        self.assertEqual(self.contract_instance.functions.currentSupply().call(), 0)

    def test_adjust_supply(self):
       self.contract_instance.functions.adjustSupply(1000).transact({'from': self.account})
        self.assertEqual(self.contract_instance.functions.currentSupply().call(), 1000)

    def test_adjust_supply_negative(self):
        with self.assertRaises(ValueError):
            self.contract_instance.functions.adjustSupply(-500).transact({'from': self.account})

if __name__ == '__main__':
    unittest.main()
