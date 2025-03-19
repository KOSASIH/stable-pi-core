import os
import json
import logging
from web3 import Web3
from eth_account import Account
from cryptography.fernet import Fernet

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WalletSolutions:
    def __init__(self, storage_path):
        self.storage_path = storage_path
        self.wallets = {}
        self.encryption_key = None

    def generate_encryption_key(self):
        """Generate a symmetric encryption key for secure storage of private keys."""
        self.encryption_key = Fernet.generate_key()
        logging.info("Encryption key generated.")

    def save_encryption_key(self, key_path):
        """Save the encryption key to a file."""
        with open(key_path, 'wb') as f:
            f.write(self.encryption_key)
        logging.info("Encryption key saved to file.")

    def load_encryption_key(self, key_path):
        """Load the encryption key from a file."""
        with open(key_path, 'rb') as f:
            self.encryption_key = f.read()
        logging.info("Encryption key loaded from file.")

    def create_wallet(self, wallet_name):
        """Create a new Ethereum wallet and store the private key securely."""
        account = Account.create()
        private_key = account.privateKey.hex()
        address = account.address

        # Encrypt the private key
        fernet = Fernet(self.encryption_key)
        encrypted_private_key = fernet.encrypt(private_key.encode('utf-8'))

        # Store the wallet information
        self.wallets[wallet_name] = {
            'address': address,
            'encrypted_private_key': encrypted_private_key
        }

        # Save the wallet to a file
        self.save_wallet(wallet_name)
        logging.info(f"Wallet '{wallet_name}' created with address: {address}")

    def save_wallet(self, wallet_name):
        """Save the wallet information to a JSON file."""
        wallet_file_path = os.path.join(self.storage_path, f"{wallet_name}.json")
        with open(wallet_file_path, 'w') as f:
            json.dump(self.wallets[wallet_name], f)
        logging.info(f"Wallet '{wallet_name}' saved to file.")

    def load_wallet(self, wallet_name):
        """Load a wallet from a JSON file."""
        wallet_file_path = os.path.join(self.storage_path, f"{wallet_name}.json")
        if os.path.exists(wallet_file_path):
            with open(wallet_file_path, 'r') as f:
                wallet_data = json.load(f)
                self.wallets[wallet_name] = wallet_data
                logging.info(f"Wallet '{wallet_name}' loaded from file.")
        else:
            logging.error(f"Wallet '{wallet_name}' does not exist.")

    def get_private_key(self, wallet_name):
        """Retrieve the decrypted private key for a wallet."""
        if wallet_name in self.wallets:
            fernet = Fernet(self.encryption_key)
            encrypted_private_key = self.wallets[wallet_name]['encrypted_private_key']
            private_key = fernet.decrypt(encrypted_private_key).decode('utf-8')
            logging.info(f"Private key retrieved for wallet '{wallet_name}'.")
            return private_key
        else:
            logging.error(f"Wallet '{wallet_name}' not found.")
            return None

    def send_transaction(self, wallet_name, recipient, amount, gas_price=20000000000):
        """Send a transaction from the specified wallet to a recipient."""
        private_key = self.get_private_key(wallet_name)
        if private_key is None:
            return

        # Create a Web3 instance
        web3 = Web3(Web3.HTTPProvider('https://your-ethereum-node-url'))

        # Prepare the transaction
        account = Account.from_key(private_key)
        transaction = {
            'to': recipient,
            'value': web3.toWei(amount, 'ether'),
            'gas': 2000000,
            'gasPrice': gas_price,
            'nonce': web3.eth.getTransactionCount(account.address),
            'chainId': 1  # Mainnet
        }

        # Sign the transaction
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key)

        # Send the transaction
        tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        logging.info(f"Transaction sent! TX Hash: {web3.toHex(tx_hash)}")

    def run(self):
        """Example usage of the wallet solutions."""
        # Generate and save an encryption key
        self.generate_encryption_key()
        self.save_encryption_key('encryption_key.key')

        # Load the encryption key
        self load_encryption_key('encryption_key.key')

        # Create a new wallet
        self.create_wallet('my_wallet')

        # Load the wallet
        self.load_wallet('my_wallet')

        # Retrieve the private key
        private_key = self.get_private_key('my_wallet')

        # Send a transaction
        recipient_address = '0xRecipientAddress'
        amount_to_send = 0.01  # Amount in Ether
        self.send_transaction('my_wallet', recipient_address, amount_to_send)

if __name__ == "__main__":
    wallet_solutions = WalletSolutions(storage_path='./wallets')
    wallet_solutions.run()
