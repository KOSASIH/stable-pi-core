from web3 import Web3
from utils.config import Config

# Load configuration
config = Config('config.json')
eth_node = config.get('eth_node')
web3 = Web3(Web3.HTTPProvider(eth_node))

# Wallet class to manage Ethereum wallet operations
class Wallet:
    def __init__(self, private_key):
        self.private_key = private_key
        self.account = web3.eth.account.from_key(private_key)

    def get_balance(self):
        """Get the balance of the wallet in Ether."""
        balance_wei = web3.eth.get_balance(self.account.address)
        return web3.fromWei(balance_wei, 'ether')

    def send_transaction(self, to_address, amount):
        """Send Ether from this wallet to another address."""
        nonce = web3.eth.getTransactionCount(self.account.address)
        tx = {
            'to': to_address,
            'value': web3.toWei(amount, 'ether'),
            'gas': 2000000,
            'gasPrice': web3.toWei('50', 'gwei'),
            'nonce': nonce,
            'chainId': 1  # Mainnet
        }
        signed_tx = web3.eth.account.sign_transaction(tx, self.private_key)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return web3.toHex(tx_hash)

# Example usage
if __name__ == "__main__":
    # Replace with your actual private key
    private_key = '0xYourPrivateKeyHere'
    wallet = Wallet(private_key)

    print(f"Wallet Address: {wallet.account.address}")
    print(f"Current Balance: {wallet.get_balance()} ETH")

    # Example transaction (replace with a valid address and amount)
    to_address = '0xRecipientAddressHere'
    amount = 0.01  # Amount in Ether
    tx_hash = wallet.send_transaction(to_address, amount)
    print(f"Transaction sent! Hash: {tx_hash}")
