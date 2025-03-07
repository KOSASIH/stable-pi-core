import logging
from web3 import Web3

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Layer2Solutions:
    def __init__(self, provider_url):
        """Initialize Layer-2 solutions with a Web3 provider."""
        self.web3 = Web3(Web3.HTTPProvider(provider_url))
        if not self.web3.isConnected():
            logging.error("Failed to connect to the Layer-2 network.")
            raise ConnectionError("Unable to connect to the Layer-2 network.")
        logging.info("Connected to Layer-2 network.")

    def send_transaction(self, from_address, private_key, to_address, amount):
        """Send a transaction using Layer-2 solution."""
        try:
            # Prepare the transaction
            nonce = self.web3.eth.getTransactionCount(from_address)
            tx = {
                'to': to_address,
                'value': self.web3.toWei(amount, 'ether'),
                'gas': 2000000,
                'gasPrice': self.web3.toWei('50', 'gwei'),
                'nonce': nonce,
                'chainId': 1  # Change to the appropriate chain ID for Layer-2
            }

            # Sign the transaction
            signed_tx = self.web3.eth.account.signTransaction(tx, private_key)

            # Send the transaction
            tx_hash = self.web3.eth.sendRawTransaction(signed_tx.rawTransaction)
            logging.info(f"Transaction sent: {tx_hash.hex()}")
            return tx_hash.hex()
        except Exception as e:
            logging.error(f"Error sending transaction: {e}")
            raise

    def check_transaction_status(self, tx_hash):
        """Check the status of a transaction."""
        try:
            tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
            if tx_receipt.status == 1:
                logging.info(f"Transaction {tx_hash} was successful.")
            else:
                logging.warning(f"Transaction {tx_hash} failed.")
            return tx_receipt
        except Exception as e:
            logging.error(f"Error checking transaction status: {e}")
            raise

# Example usage
if __name__ == "__main__":
    # Replace with your Layer-2 provider URL
    provider_url = "https://your-layer2-node-url"
    layer2 = Layer2Solutions(provider_url)

    # Example transaction details
    from_address = "0xYourAddress"
    private_key = "YourPrivateKey"
    to_address = "0xRecipientAddress"
    amount = 0.1  # Amount in Ether

    # Send a transaction
    try:
        tx_hash = layer2.send_transaction(from_address, private_key, to_address, amount)
        print(f"Transaction Hash: {tx_hash}")

        # Check transaction status
        layer2.check_transaction_status(tx_hash)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
