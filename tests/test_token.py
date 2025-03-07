import pytest
from web3 import Web3
from solcx import compile_source

# Sample Solidity code for the Token contract
TOKEN_CONTRACT_SOURCE = '''
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Token is ERC20, Ownable {
    mapping(address => bool) public minters;

    event MinterAdded(address indexed account);
    event MinterRemoved(address indexed account);

    constructor(string memory name, string memory symbol) ERC20(name, symbol) {}

    modifier onlyMinter() {
        require(minters[msg.sender], "Caller is not a minter");
        _;
    }

    function addMinter(address account) external onlyOwner {
        minters[account] = true;
        emit MinterAdded(account);
    }

    function removeMinter(address account) external onlyOwner {
        minters[account] = false;
        emit MinterRemoved(account);
    }

    function mint(address to, uint256 amount) external onlyMinter {
        _mint(to, amount);
    }

    function burn(uint256 amount) external {
        _burn(msg.sender, amount);
    }
}
'''

@pytest.fixture
def token_contract(web3):
    # Compile the contract
    compiled_sol = compile_source(TOKEN_CONTRACT_SOURCE)
    contract_interface = compiled_sol['<stdin>:Token']

    # Deploy the contract
    TokenContract = web3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])
    tx_hash = TokenContract.constructor("Stable Pi Token", "SPT").transact({'from': web3.eth.accounts[0]})
    tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

    return web3.eth.contract(address=tx_receipt.contractAddress, abi=contract_interface['abi'])

def test_initial_supply(token_contract):
    # Assert initial supply is zero
    assert token_contract.functions.totalSupply().call() == 0

def test_minting(token_contract):
    # Arrange
    owner = token_contract.functions.owner().call()
    token_contract.functions.addMinter(web3.eth.accounts[1]).transact({'from': owner})

    # Act
    tx_hash = token_contract.functions.mint(web3.eth.accounts[2], 100).transact({'from': web3.eth.accounts[1]})
    web3.eth.waitForTransactionReceipt(tx_hash)

    # Assert
    assert token_contract.functions.balanceOf(web3.eth.accounts[2]).call() == 100
    assert token_contract.functions.totalSupply().call() == 100

def test_burning(token_contract):
    # Arrange
    owner = token_contract.functions.owner().call()
    token_contract.functions.addMinter(web3.eth.accounts[1]).transact({'from': owner})
    token_contract.functions.mint(web3.eth.accounts[2], 100).transact({'from': web3.eth.accounts[1]})

    # Act
    tx_hash = token_contract.functions.burn(50).transact({'from': web3.eth.accounts[2]})
    web3.eth.waitForTransactionReceipt(tx_hash)

    # Assert
    assert token_contract.functions.balanceOf(web3.eth.accounts[2]).call() == 50
    assert token_contract.functions.totalSupply().call() == 50

def test_add_minter(token_contract):
    # Arrange
    owner = token_contract.functions.owner().call()

    # Act
    tx_hash = token_contract.functions.addMinter(web3.eth.accounts[1]).transact({'from': owner})
    web3.eth.waitForTransactionReceipt(tx_hash)

    # Assert
    assert token_contract.functions.minters(web3.eth.accounts[1]).call() is True

def test_remove_minter(token_contract):
    # Arrange
    owner = token_contract.functions.owner().call()
    token_contract.functions.addMinter(web3.eth.accounts[1]).transact({'from': owner})

    # Act
    tx_hash = token_contract.functions.removeMinter(web3.eth.accounts[1]).transact({'from': owner})
    web3.eth.waitForTransactionReceipt(tx_hash)

    # Assert
    assert token_contract.functions.minters(web3.eth.accounts[1]).call() is False

def test_minting_without_permission(token_contract):
    # Act & Assert
    with pytest.raises(Exception):
        token_contract.functions.mint(web3.eth.accounts[2], 100).transact({'from': web3.eth.accounts[3]})

def test_burn_more_than_balance(token_contract):
    # Arrange
    owner = token_contract.functions.owner().call()
    token_contract.functions.addMinter(web3.eth.accounts[1]).transact({'from': owner})
    token_contract.functions.mint(web3.eth.accounts[2], 100).transact({'from': web3.eth.accounts[1]})

    # Act & Assert
    with pytest.raises(Exception):
        token_contract.functions.burn(200).transact({'from': web3.eth .accounts[2]})

def test_burn_without_balance(token_contract):
    # Act & Assert
    with pytest.raises(Exception):
        token_contract.functions.burn(50).transact({'from': web3.eth.accounts[3]})

def test_transfer(token_contract):
    # Arrange
    owner = token_contract.functions.owner().call()
    token_contract.functions.addMinter(web3.eth.accounts[1]).transact({'from': owner})
    token_contract.functions.mint(web3.eth.accounts[2], 100).transact({'from': web3.eth.accounts[1]})

    # Act
    tx_hash = token_contract.functions.transfer(web3.eth.accounts[3], 50).transact({'from': web3.eth.accounts[2]})
    web3.eth.waitForTransactionReceipt(tx_hash)

    # Assert
    assert token_contract.functions.balanceOf(web3.eth.accounts[2]).call() == 50
    assert token_contract.functions.balanceOf(web3.eth.accounts[3]).call() == 50

def test_transfer_more_than_balance(token_contract):
    # Arrange
    owner = token_contract.functions.owner().call()
    token_contract.functions.addMinter(web3.eth.accounts[1]).transact({'from': owner})
    token_contract.functions.mint(web3.eth.accounts[2], 100).transact({'from': web3.eth.accounts[1]})

    # Act & Assert
    with pytest.raises(Exception):
        token_contract.functions.transfer(web3.eth.accounts[3], 200).transact({'from': web3.eth.accounts[2]})

def test_approve_and_transfer_from(token_contract):
    # Arrange
    owner = token_contract.functions.owner().call()
    token_contract.functions.addMinter(web3.eth.accounts[1]).transact({'from': owner})
    token_contract.functions.mint(web3.eth.accounts[2], 100).transact({'from': web3.eth.accounts[1]})

    # Act
    tx_hash = token_contract.functions.approve(web3.eth.accounts[3], 50).transact({'from': web3.eth.accounts[2]})
    web3.eth.waitForTransactionReceipt(tx_hash)

    # Transfer from
    tx_hash = token_contract.functions.transferFrom(web3.eth.accounts[2], web3.eth.accounts[4], 50).transact({'from': web3.eth.accounts[3]})
    web3.eth.waitForTransactionReceipt(tx_hash)

    # Assert
    assert token_contract.functions.balanceOf(web3.eth.accounts[2]).call() == 50
    assert token_contract.functions.balanceOf(web3.eth.accounts[4]).call() == 50

def test_transfer_from_without_approval(token_contract):
    # Arrange
    owner = token_contract.functions.owner().call()
    token_contract.functions.addMinter(web3.eth.accounts[1]).transact({'from': owner})
    token_contract.functions.mint(web3.eth.accounts[2], 100).transact({'from': web3.eth.accounts[1]})

    # Act & Assert
    with pytest.raises(Exception):
        token_contract.functions.transferFrom(web3.eth.accounts[2], web3.eth.accounts[4], 50).transact({'from': web3.eth.accounts[3]})

def test_approve_more_than_balance(token_contract):
    # Arrange
    owner = token_contract.functions.owner().call()
    token_contract.functions.addMinter(web3.eth.accounts[1]).transact({'from': owner})
    token_contract.functions.mint(web3.eth.accounts[2], 100).transact({'from': web3.eth.accounts[1]})

    # Act
    tx_hash = token_contract.functions.approve(web3.eth.accounts[3], 150).transact({'from': web3.eth.accounts[2]})
    web3.eth.waitForTransactionReceipt(tx_hash)

    # Assert
    assert token_contract.functions.allowance(web3.eth.accounts[2], web3.eth.accounts[3]).call() == 150
