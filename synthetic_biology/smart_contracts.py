from web3 import Web3
from solcx import compile_source
import json

class SmartContractManager:
    """
    A class to manage smart contracts for handling biosensor data.

    Attributes:
        web3 (Web3): An instance of the Web3 class for interacting with the blockchain.
        contract (Contract): The deployed smart contract instance.
        contract_address (str): The address of the deployed smart contract.
    """

    def __init__(self, blockchain_url: str, contract_source: str):
        self.web3 = Web3(Web3.HTTPProvider(blockchain_url))
        self.contract = None
        self.contract_address = None
        self.compile_contract(contract_source)

    def compile_contract(self, contract_source: str):
        """
        Compiles the smart contract source code.

        Args:
            contract_source (str): The Solidity source code of the smart contract.
        """
        compiled_sol = compile_source(contract_source)
        contract_id, contract_interface = compiled_sol.popitem()
        self.contract = self.web3.eth.contract(
            address=self.contract_address,
            abi=contract_interface['abi']
        )

    def deploy_contract(self, account: str, private_key: str) -> str:
        """
        Deploys the smart contract to the blockchain.

        Args:
            account (str): The account address to deploy the contract from.
            private_key (str): The private key of the account.

        Returns:
            str: The address of the deployed smart contract.
        """
        # Prepare the transaction
        transaction = self.contract.constructor().buildTransaction({
            'from': account,
            'nonce': self.web3.eth.getTransactionCount(account),
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei')
        })

        # Sign the transaction
        signed_txn = self.web3.eth.account.signTransaction(transaction, private_key)

        # Send the transaction
        tx_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)

        # Wait for the transaction to be mined
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)

        self.contract_address = tx_receipt.contractAddress
        return self.contract_address

    def log_data(self, sensor_id: str, timestamp: str, value: float, unit: str):
        """
        Logs biosensor data to the smart contract.

        Args:
            sensor_id (str): The ID of the biosensor.
            timestamp (str): The timestamp of the data.
            value (float): The value of the data.
            unit (str): The unit of measurement.
        """
        if not self.contract_address:
            raise Exception("Smart contract is not deployed.")

        transaction = self.contract.functions.logData(sensor_id, timestamp, value, unit).buildTransaction({
            'from': self.web3.eth.defaultAccount,
            'nonce': self.web3.eth.getTransactionCount(self.web3.eth.defaultAccount),
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei')
        })

        signed_txn = self.web3.eth.account.signTransaction(transaction, self.web3.eth.defaultAccount.privateKey)
        tx_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        self.web3.eth.waitForTransactionReceipt(tx_hash)

    def get_data(self, sensor_id: str):
        """
        Retrieves biosensor data from the smart contract.

        Args:
            sensor_id (str): The ID of the biosensor.

        Returns:
            dict: The data associated with the biosensor.
        """
        if not self.contract_address:
            raise Exception("Smart contract is not deployed.")

        return self.contract.functions.getData(sensor_id).call()
