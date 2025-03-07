import os
import json
import time
import logging
from web3 import Web3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
ETHEREUM_RPC_URL = os.getenv('ETHEREUM_RPC_URL')
BSC_RPC_URL = os.getenv('BSC_RPC_URL')
ETHEREUM_CONTRACT_ADDRESS = os.getenv('ETHEREUM_CONTRACT_ADDRESS')
BSC_CONTRACT_ADDRESS = os.getenv('BSC_CONTRACT_ADDRESS')
BSC_PRIVATE_KEY = os.getenv('BSC_PRIVATE_KEY')

# Connect to Ethereum and BSC
eth_web3 = Web3(Web3.HTTPProvider(ETHEREUM_RPC_URL))
bsc_web3 = Web3(Web3.HTTPProvider(BSC_RPC_URL))

# Load the contract ABI
with open('EthereumBridgeDAO.json', 'r') as f:
    eth_contract_data = json.load(f)

with open('BSCBridgeDAO.json', 'r') as f:
    bsc_contract_data = json.load(f)

# Create contract instances
eth_contract = eth_web3.eth.contract(address=ETHEREUM_CONTRACT_ADDRESS, abi=eth_contract_data['abi'])
bsc_contract = bsc_web3.eth.contract(address=BSC_CONTRACT_ADDRESS, abi=bsc_contract_data['abi'])

# Function to unlock tokens on BSC
def unlock_tokens(user, amount):
    try:
        # Prepare the transaction
        tx = bsc_contract.functions.unlockTokens(user, amount).buildTransaction({
            'from': bsc_web3.eth.accounts[0],  # Replace with your BSC account
            'gas': 2000000,
            'gasPrice': bsc_web3.toWei('5', 'gwei'),
            'nonce': bsc_web3.eth.getTransactionCount(bsc_web3.eth.accounts[0]),
        })

        # Sign and send the transaction
        signed_tx = bsc_web3.eth.account.signTransaction(tx, private_key=BSC_PRIVATE_KEY)
        tx_hash = bsc_web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        logging.info(f'Tokens unlocked for {user}. Transaction hash: {tx_hash.hex()}')
    except Exception as e:
        logging.error(f'Error unlocking tokens for {user}: {e}')

# Event listener for TokensLocked event
def handle_tokens_locked(event):
    user = event['args']['user']
    amount = event['args']['amount']
    logging.info(f'Tokens locked: {amount} by {user}. Unlocking on BSC...')
    unlock_tokens(user, amount)

# Main loop to listen for events
def main():
    logging.info('Listening for TokensLocked events...')
    while True:
        try:
            # Create a filter for the TokensLocked event
            event_filter = eth_contract.events.TokensLocked.createFilter(fromBlock='latest')
            for event in event_filter.get_new_entries():
                handle_tokens_locked(event)
            time.sleep(10)  # Polling interval
        except Exception as e:
            logging.error(f'Error in event listening loop: {e}')
            time.sleep(5)  # Wait before retrying

if __name__ == '__main__':
    main()
