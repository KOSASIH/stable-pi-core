import os
import json
import logging
from web3 import Web3
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Connect to Ethereum network
def connect_to_ethereum():
    infura_url = os.getenv("INFURA_URL")
    if not infura_url:
        logger.error("INFURA_URL environment variable not set.")
        raise ValueError("INFURA_URL is required to connect to Ethereum.")
    
    web3 = Web3(Web3.HTTPProvider(infura_url))
    
    if not web3.isConnected():
        logger.error("Failed to connect to Ethereum network.")
        raise ConnectionError("Could not connect to Ethereum network.")
    
    logger.info("Connected to Ethereum network.")
    return web3

# Load contract ABI and bytecode
def load_contract_data(contract_name):
    try:
        with open(f'./edge-computing/chainlink/contracts/{contract_name}.json') as f:
            contract_data = json.load(f)
            return contract_data['abi'], contract_data['bytecode']
    except FileNotFoundError:
        logger.error(f"Contract file for {contract_name} not found.")
        raise
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON for contract {contract_name}.")
        raise

# Deploy the contract
def deploy_contract(web3, contract_name, account):
    abi, bytecode = load_contract_data(contract_name)
    
    # Create contract instance
    contract = web3.eth.contract(abi=abi, bytecode=bytecode)
    
    # Build transaction
    transaction = contract.constructor().buildTransaction({
        'from': account,
        'nonce': web3.eth.getTransactionCount(account),
        'gas': 2000000,
        'gasPrice': web3.toWei('50', 'gwei'),
    })
    
    # Sign the transaction
    private_key = os.getenv("PRIVATE_KEY")
    if not private_key:
        logger.error("PRIVATE_KEY environment variable not set.")
        raise ValueError("PRIVATE_KEY is required to sign the transaction.")
    
    signed_txn = web3.eth.account.signTransaction(transaction, private_key)
    
    # Send the transaction
    tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    logger.info(f"Transaction sent: {tx_hash.hex()}")
    
    # Wait for the transaction to be mined
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    logger.info(f"Contract deployed at address: {tx_receipt.contractAddress}")
    
    return tx_receipt.contractAddress

if __name__ == "__main__":
    try:
        web3 = connect_to_ethereum()
        account = os.getenv("DEPLOYER_ACCOUNT")
        if not account:
            logger.error("DEPLOYER_ACCOUNT environment variable not set.")
            raise ValueError("DEPLOYER_ACCOUNT is required for deployment.")
        
        contract_name = "price_feed_contract"  # Change to your contract name
        deploy_contract(web3, contract_name, account)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
