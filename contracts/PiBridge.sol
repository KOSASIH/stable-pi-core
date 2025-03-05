// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PiBridge {
    address public owner;
    mapping(address => uint256) public balances;

    event Deposited(address indexed user, uint256 amount);
    event Withdrawn(address indexed user, uint256 amount);
    event Bridged(address indexed user, uint256 amount, string targetChain);

    constructor() {
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can perform this action");
        _;
    }

    // Deposit Pi Coin to the bridge
    function deposit(uint256 amount) public {
        require(amount > 0, "Amount must be greater than zero");
        balances[msg.sender] += amount;
        emit Deposited(msg.sender, amount);
    }

    // Withdraw Pi Coin from the bridge
    function withdraw(uint256 amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        balances[msg.sender] -= amount;
        emit Withdrawn(msg.sender, amount);
    }

    // Bridge Pi Coin to another chain
    function bridge(uint256 amount, string memory targetChain) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        balances[msg.sender] -= amount;
        emit Bridged(msg.sender, amount, targetChain);
        // Logic to handle bridging to the target chain would go here
    }

    // Function to check user balance
    function checkBalance() public view returns (uint256) {
        return balances[msg.sender];
    }
}
