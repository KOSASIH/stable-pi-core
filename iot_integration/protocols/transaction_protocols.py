import json
import logging
from web3 import Web3

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TransactionHandler:
    def __init__(self, ethereum_node, contract_address, contract_abi, private_key):
        self.w3 = Web3(Web3.HTTPProvider(ethereum_node))
        self.contract_address = contract_address
        self.contract_abi = contract_abi
        self.private_key = private_key
        self.contract = self.w3.eth.contract(address=self.contract_address, abi=self.contract_abi)

    def create_transaction(self, from_address, amount):
        """Create a transaction to send to the Ethereum blockchain."""
        try:
            # Prepare the transaction
            tx = {
                'to': self.contract_address,
                'value': self.w3.toWei(amount, 'ether'),  # Amount in Ether
                'gas': 2000000,
                'gasPrice': self.w3.toWei('50', 'gwei'),
                'nonce': self.w3.eth.getTransactionCount(from_address),
            }
            return tx
        except Exception as e:
            logging.error(f"Error creating transaction: {e}")
            return None

    def sign_transaction(self, tx):
        """Sign the transaction with the private key."""
        try:
            signed_tx = self.w3.eth.account.signTransaction(tx, private_key=self.private_key)
            return signed_tx
        except Exception as e:
            logging.error(f"Error signing transaction: {e}")
            return None

    def send_transaction(self, signed_tx):
        """Send the signed transaction to the Ethereum blockchain."""
        try:
            tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
            logging.info(f"Transaction sent: {tx_hash.hex()}")
            return tx_hash.hex()
        except Exception as e:
            logging.error(f"Error sending transaction: {e}")
            return None

    def execute_transaction(self, from_address, amount):
        """Execute the full transaction process: create, sign, and send."""
        tx = self.create_transaction(from_address, amount)
        if tx:
            signed_tx = self.sign_transaction(tx)
            if signed_tx:
                return self.send_transaction(signed_tx)
        return None

if __name__ == "__main__":
    # Example usage
    ETHEREUM_NODE = "https://your.ethereum.node"  # Replace with your Ethereum node URL
    CONTRACT_ADDRESS = "0xYourContractAddress"     # Replace with your contract address
    CONTRACT_ABI = json.loads('[{"constant":true,"inputs":[],"name":"yourFunction","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')  # Replace with your contract ABI
    PRIVATE_KEY = "0xYourPrivateKey"               # Replace with your private key

    transaction_handler = TransactionHandler(ETHEREUM_NODE, CONTRACT_ADDRESS, CONTRACT_ABI, PRIVATE_KEY)

    from_address = "0xYourAddress"  # Replace with your Ethereum address
    amount = 0.1                    # Amount in Ether to send

    tx_hash = transaction_handler.execute_transaction(from_address, amount)
    if tx_hash:
        logging.info(f"Transaction successful with hash: {tx_hash}")
    else:
        logging.error("Transaction failed.")
