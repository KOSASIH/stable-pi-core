// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Token is ERC20, Ownable {
    // Mapping to track minters
    mapping(address => bool) public minters;

    event MinterAdded(address indexed account);
    event MinterRemoved(address indexed account);

    constructor(string memory name, string memory symbol) ERC20(name, symbol) {}

    // Modifier to check if the caller is a minter
    modifier onlyMinter() {
        require(minters[msg.sender], "Caller is not a minter");
        _;
    }

    // Function to add a new minter
    function addMinter(address account) external onlyOwner {
        minters[account] = true;
        emit MinterAdded(account);
    }

    // Function to remove a minter
    function removeMinter(address account) external onlyOwner {
        minters[account] = false;
        emit MinterRemoved(account);
    }

    // Function to mint new tokens
    function mint(address to, uint256 amount) external onlyMinter {
        _mint(to, amount);
    }

    // Function to burn tokens
    function burn(uint256 amount) external {
        _burn(msg.sender, amount);
    }
}
