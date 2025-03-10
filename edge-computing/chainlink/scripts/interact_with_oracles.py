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

# Load contract ABI
def load_contract_abi(contract_name):
    try:
        with open(f'./edge-computing/chainlink/contracts/{contract_name}.json') as f:
            contract_data = json.load(f)
            return contract_data['abi']
    except FileNotFoundError:
        logger.error(f"Contract file for {contract_name} not found.")
        raise
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON for contract {contract_name}.")
        raise

# Interact with the oracle contract
def interact_with_oracle(web3, contract_address, account):
    abi = load_contract_abi("oracle_contract")  # Change to your oracle contract name
    oracle_contract = web3.eth.contract(address=contract_address, abi=abi)

    # Example: Fetching the latest price from the oracle
    try:
        latest_price = oracle_contract.functions.getLatestPrice().call()
        logger.info(f"Latest price from oracle: {latest_price}")
    except Exception as e:
        logger.error(f"Error fetching data from oracle: {e}")
        raise

    # Example: Requesting new data from the oracle
    try:
        tx = oracle_contract.functions.requestNewData().buildTransaction({
            'from': account,
            'nonce': web3.eth.getTransactionCount(account),
            'gas': 200000,
            'gasPrice': web3.toWei('50', 'gwei'),
        })

        private_key = os.getenv("PRIVATE_KEY")
        if not private_key:
            logger.error("PRIVATE_KEY environment variable not set.")
            raise ValueError("PRIVATE_KEY is required to sign the transaction.")

        signed_txn = web3.eth.account.signTransaction(tx, private_key)
        tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        logger.info(f"Transaction sent to request new data: {tx_hash.hex()}")

        # Wait for the transaction to be mined
        tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
        logger.info(f"Transaction receipt: {tx_receipt}")
    except Exception as e:
        logger.error(f"Error requesting new data from oracle: {e}")
        raise

if __name__ == "__main__":
    try:
        web3 = connect_to_ethereum()
        account = os.getenv("DEPLOYER_ACCOUNT")
        if not account:
            logger.error("DEPLOYER_ACCOUNT environment variable not set.")
            raise ValueError("DEPLOYER_ACCOUNT is required for interaction.")

        oracle_contract_address = "0xYourOracleContractAddress"  # Replace with your oracle contract address
        interact_with_oracle(web3, oracle_contract_address, account)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
