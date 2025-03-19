from web3 import Web3
import json

class BlockchainInterface:
    def __init__(self, infura_url, contract_address, contract_abi, private_key, account_address):
        # Connect to Ethereum network
        self.web3 = Web3(Web3.HTTPProvider(infura_url))
        if not self.web3.isConnected():
            raise Exception("Failed to connect to the Ethereum network")

        # Load smart contract
        self.contract_address = contract_address
        self.contract_abi = contract_abi
        self.contract = self.web3.eth.contract(address=self.contract_address, abi=self.contract_abi)

        # User account details
        self.private_key = private_key
        self.account_address = account_address

    def send_transaction(self, function_name, *args):
        """Send a transaction to the smart contract."""
        nonce = self.web3.eth.getTransactionCount(self.account_address)
        transaction = self.contract.functions[function_name](*args).buildTransaction({
            'chainId': 1,  # Mainnet
            'gas': 2000000,
            'gasPrice': self.web3.toWei('50', 'gwei'),
            'nonce': nonce,
        })

        # Sign the transaction
        signed_txn = self.web3.eth.account.signTransaction(transaction, private_key=self.private_key)

        # Send the transaction
        txn_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return self.web3.toHex(txn_hash)

    def get_balance(self):
        """Get the balance of the account."""
        balance_wei = self.web3.eth.getBalance(self.account_address)
        return self.web3.fromWei(balance_wei, 'ether')

    def call_contract_function(self, function_name, *args):
        """Call a read-only function from the smart contract."""
        return self.contract.functions[function_name](*args).call()

    def get_transaction_receipt(self, txn_hash):
        """Get the transaction receipt."""
        return self.web3.eth.getTransactionReceipt(txn_hash)

# Example usage
if __name__ == "__main__":
    # Replace with your Ethereum account details and contract information
    INFURA_URL = 'https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID'
    CONTRACT_ADDRESS = '0xYourSmartContractAddress'
    
    with open('path/to/your/contract_abi.json') as f:
        CONTRACT_ABI = json.load(f)

    PRIVATE_KEY = 'YOUR_PRIVATE_KEY'
    ACCOUNT_ADDRESS = '0xYourAccountAddress'

    blockchain_interface = BlockchainInterface(INFURA_URL, CONTRACT_ADDRESS, CONTRACT_ABI, PRIVATE_KEY, ACCOUNT_ADDRESS)

    # Example: Send a transaction to a smart contract function
    try:
        txn_hash = blockchain_interface.send_transaction('storeQuantumData', {'qubit_state': '0b1010', 'metadata': 'Quantum data'})
        print(f'Transaction sent with hash: {txn_hash}')
    except Exception as e:
        print(f'Error sending transaction: {e}')

    # Example: Get account balance
    balance = blockchain_interface.get_balance()
    print(f'Account balance: {balance} ETH')

    # Example: Call a read-only function from the smart contract
    try:
        quantum_data = blockchain_interface.call_contract_function('getQuantumData', 1)
        print(f'Retrieved quantum data: {quantum_data}')
    except Exception as e:
        print(f'Error retrieving quantum data: {e}')
