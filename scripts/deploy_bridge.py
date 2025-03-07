import os
import json
import logging
from web3 import Web3
from solcx import compile_source

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Smart contract source code for Ethereum Bridge
ETHEREUM_BRIDGE_SOURCE = '''
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract EthereumBridgeDAO is Ownable {
    struct LockedToken {
        address user;
        uint256 amount;
        string destinationChain;
    }

    IERC20 public token;
    mapping(uint256 => LockedToken) public lockedTokens;
    uint256 public lockedTokenCount;

    event TokensLocked(address indexed user, uint256 amount, string destinationChain, uint256 indexed lockId);

    constructor(address _token) {
        require(_token != address(0), "Token address cannot be zero");
        token = IERC20(_token);
    }

    function lockTokens(uint256 amount, string memory destinationChain) external {
        require(amount > 0, "Amount must be greater than zero");
        require(token.balanceOf(msg.sender) >= amount, "Insufficient balance");

        token.transferFrom(msg.sender, address(this), amount);
        lockedTokens[lockedTokenCount] = LockedToken(msg.sender, amount, destinationChain);
        emit TokensLocked(msg.sender, amount, destinationChain, lockedTokenCount);
        lockedTokenCount++;
    }
}
'''

# Smart contract source code for BSC Bridge
BSC_BRIDGE_SOURCE = '''
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract BSCBridgeDAO is Ownable {
    IERC20 public token;

    event TokensUnlocked(address indexed user, uint256 amount);

    constructor(address _token) {
        require(_token != address(0), "Token address cannot be zero");
        token = IERC20(_token);
    }

    function unlockTokens(address user, uint256 amount) external onlyOwner {
        require(amount > 0, "Amount must be greater than zero");
        token.transfer(user, amount);
        emit TokensUnlocked(user, amount);
    }
}
'''

def deploy_contract(w3, contract_source, token_address):
    try:
        # Compile the contract
        compiled_sol = compile_source(contract_source)
        contract_interface = compiled_sol['<stdin>:EthereumBridgeDAO'] if 'EthereumBridgeDAO' in contract_source else compiled_sol['<stdin>:BSCBridgeDAO']

        # Set up the account to deploy the contract
        account = w3.eth.accounts[0]
        w3.eth.defaultAccount = account

        # Deploy the contract
        bridge_contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
        tx_hash = bridge_contract.constructor(token_address).transact()
        tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

        logging.info(f"Contract deployed at address: {tx_receipt.contractAddress}")
        return tx_receipt.contractAddress
    except Exception as e:
        logging.error(f"Error deploying contract: {e}")
        return None

def main():
    # Load environment variables
    ETHEREUM_RPC_URL = os.getenv('ETHEREUM_RPC_URL')
    BSC_RPC_URL = os.getenv('BSC_RPC_URL')
    TOKEN_ADDRESS = os.getenv('TOKEN_ADDRESS')

    # Connect to Ethereum
    eth_w3 = Web3(Web3.HTTPProvider(ETHEREUM_RPC_URL))
    if not eth_w3.isConnected():
        logging.error("Failed to connect to Ethereum")
        return

    # Connect to BSC
    bsc_w3 = Web3(Web3.HTTPProvider(BSC_RPC_URL))
    if not bsc_w3.isConnected():
        logging.error("Failed to connect to BSC")
        return

    # Deploy Ethereum Bridge
    logging.info("Deploying Ethereum Bridge...")
    eth_bridge_address = deploy_contract(eth_w3, ETHEREUM_BRIDGE_SOURCE, TOKEN_ADDRESS)

    # Deploy BSC Bridge
    logging.info("Deploying BSC Bridge...")
    bsc_bridge_address = deploy_contract(bsc_w3, BSC_BRIDGE_SOURCE, TOKEN_ADDRESS)

    if eth_bridge_address:
        logging.info(f"Ethereum Bridge deployed at: {eth_bridge_address}")
    if bsc_bridge_address:
        logging.info(f"BSC Bridge deployed at: {bsc_bridge_address}")

if __name__ == '__main__':
    main()
