import os
import pytest
from web3 import Web3
from dotenv import load_dotenv
from deploy_contracts import deploy_contract  # Import the deploy function
from interact_with_oracles import interact_with_oracle  # Import the interaction function

# Load environment variables from a .env file
load_dotenv()

@pytest.fixture(scope="module")
def web3():
    """Fixture to create a Web3 connection."""
    infura_url = os.getenv("INFURA_URL")
    web3 = Web3(Web3.HTTPProvider(infura_url))
    assert web3.isConnected(), "Failed to connect to Ethereum network."
    return web3

@pytest.fixture(scope="module")
def deployer_account():
    """Fixture to provide the deployer account."""
    account = os.getenv("DEPLOYER_ACCOUNT")
    assert account, "DEPLOYER_ACCOUNT environment variable not set."
    return account

@pytest.fixture(scope="module")
def oracle_contract(web3, deployer_account):
    """Fixture to deploy the oracle contract."""
    contract_name = "oracle_contract"  # Change to your contract name
    contract_address = deploy_contract(web3, contract_name, deployer_account)
    yield contract_address
    # Optionally, you can add code here to clean up after tests, like destroying the contract

def test_get_latest_price(web3, oracle_contract):
    """Test fetching the latest price from the oracle."""
    abi = load_contract_abi("oracle_contract")  # Load the ABI for the oracle contract
    oracle_instance = web3.eth.contract(address=oracle_contract, abi=abi)

    # Call the function to get the latest price
    latest_price = oracle_instance.functions.getLatestPrice().call()
    assert isinstance(latest_price, (int, float)), "Latest price should be a number."
    assert latest_price > 0, "Latest price should be greater than zero."

def test_request_new_data(web3, oracle_contract, deployer_account):
    """Test requesting new data from the oracle."""
    abi = load_contract_abi("oracle_contract")  # Load the ABI for the oracle contract
    oracle_instance = web3.eth.contract(address=oracle_contract, abi=abi)

    # Build and send the transaction to request new data
    tx = oracle_instance.functions.requestNewData().buildTransaction({
        'from': deployer_account,
        'nonce': web3.eth.getTransactionCount(deployer_account),
        'gas': 200000,
        'gasPrice': web3.toWei('50', 'gwei'),
    })

    private_key = os.getenv("PRIVATE_KEY")
    signed_txn = web3.eth.account.signTransaction(tx, private_key)
    tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)

    # Wait for the transaction to be mined
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
    assert tx_receipt.status == 1, "Transaction failed."

    # Optionally, verify that the new data has been updated
    # This part depends on your contract's implementation
    # latest_price = oracle_instance.functions.getLatestPrice().call()
    # assert latest_price is not None, "Latest price should be updated."

if __name__ == "__main__":
    pytest.main()
