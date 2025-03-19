// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract Reserve is Ownable {
    using SafeMath for uint256;

    // Mapping to store reserves for each user by asset
    mapping(address => mapping(address => uint256)) private reserves; // user => token => amount

    // Event to log deposits
    event Deposited(address indexed user, address indexed token, uint256 amount);
    
    // Event to log withdrawals
    event Withdrawn(address indexed user, address indexed token, uint256 amount);
    
    // Event for emergency withdrawal
    event EmergencyWithdrawn(address indexed owner, address indexed token, uint256 amount);

    // Function to deposit ERC20 tokens into the reserve
    function deposit(address token, uint256 amount) external {
        require(amount > 0, "Deposit amount must be greater than 0");
        require(IERC20(token).transferFrom(msg.sender, address(this), amount), "Transfer failed");

        reserves[msg.sender][token] = reserves[msg.sender][token].add(amount);
        emit Deposited(msg.sender, token, amount);
    }

    // Function to withdraw ERC20 tokens from the reserve
    function withdraw(address token, uint256 amount) external {
        require(amount > 0, "Withdrawal amount must be greater than 0");
        require(reserves[msg.sender][token] >= amount, "Insufficient reserves");

        reserves[msg.sender][token] = reserves[msg.sender][token].sub(amount);
        require(IERC20(token).transfer(msg.sender, amount), "Transfer failed");
        emit Withdrawn(msg.sender, token, amount);
    }

    // Function to check the reserve balance of a user for a specific token
    function getReserveBalance(address user, address token) external view returns (uint256) {
        return reserves[user][token];
    }

    // Emergency withdrawal function for the owner
    function emergencyWithdraw(address token, uint256 amount) external onlyOwner {
        require(amount > 0, "Withdrawal amount must be greater than 0");
        require(IERC20(token).balanceOf(address(this)) >= amount, "Insufficient contract balance");

        require(IERC20(token).transfer(owner(), amount), "Transfer failed");
        emit EmergencyWithdrawn(owner(), token, amount);
    }

    // Function to get the total reserve balance of the contract for a specific token
    function getTotalReserve(address token) external view returns (uint256) {
        return IERC20(token).balanceOf(address(this));
    }
}
