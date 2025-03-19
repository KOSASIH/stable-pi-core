// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract PiConverter is Ownable, Pausable, ReentrancyGuard {
    using SafeMath for uint256;

    mapping(address => uint256) public balances;
    uint256 public conversionRate; // Conversion rate from GCV to market price
    address public feeCollector; // Address to collect fees

    event Deposited(address indexed user, uint256 amount, uint256 newBalance);
    event Converted(address indexed user, uint256 amount, uint256 convertedAmount, uint256 fee);
    event ConversionRateUpdated(uint256 newRate);
    event FeeCollectorUpdated(address newFeeCollector);
    event EmergencyWithdrawal(address indexed to, uint256 amount);

    constructor() {
        conversionRate = 314159; // Set initial conversion rate to $314,159.00
        feeCollector = msg.sender; // Set initial fee collector to contract deployer
    }

    // Function to deposit Pi Coin into the contract
    function deposit(uint256 amount) public whenNotPaused nonReentrant {
        require(amount > 0, "Amount must be greater than zero");
        balances[msg.sender] = balances[msg.sender].add(amount);
        emit Deposited(msg.sender, amount, balances[msg.sender]);
    }

    // Function to convert Pi Coin to market price
    function convert(uint256 amount) public whenNotPaused nonReentrant {
        require(amount > 0, "Amount must be greater than zero");
        require(balances[msg.sender] >= amount, "Insufficient balance");
        
        uint256 convertedAmount = amount.mul(conversionRate); // Calculate converted amount
        uint256 fee = calculateFee(convertedAmount); // Calculate fee based on dynamic structure
        uint256 netAmount = convertedAmount.sub(fee); // Net amount after fee

        require(address(this).balance >= fee, "Insufficient contract balance to pay fee");

        balances[msg.sender] = balances[msg.sender].sub(amount); // Deduct the amount from user's balance
        payable(feeCollector).transfer(fee); // Transfer fee to fee collector

        emit Converted(msg.sender, amount, netAmount, fee);
    }

    // Function to calculate fee based on the converted amount
    function calculateFee(uint256 convertedAmount) internal view returns (uint256) {
        if (convertedAmount < 1000 ether) {
            return convertedAmount.mul(1).div(100); // 1% fee for amounts less than 1000
        } else if (convertedAmount < 10000 ether) {
            return convertedAmount.mul(0.5).div(100); // 0.5% fee for amounts between 1000 and 10000
        } else {
            return convertedAmount.mul(0.1).div(100); // 0.1% fee for amounts above 10000
        }
    }

    // Function to update the conversion rate
    function updateConversionRate(uint256 newRate) public onlyOwner {
        conversionRate = newRate;
        emit ConversionRateUpdated(newRate);
    }

    // Function to update the fee collector address
    function updateFeeCollector(address newFeeCollector) public onlyOwner {
        feeCollector = newFeeCollector;
        emit FeeCollectorUpdated(newFeeCollector);
    }

    // Emergency withdrawal function for the owner
    function emergencyWithdraw(address to, uint256 amount) public onlyOwner {
        require(amount <= address(this).balance, "Insufficient contract balance");
        payable(to).transfer(amount);
        emit EmergencyWithdrawal(to, amount);
    }

    // Function to check the balance of a user
    function checkBalance() public view returns (uint256) {
        return balances[msg.sender];
    }

    // Function to pause the contract
    function pause() public onlyOwner {
        _pause();
    }

    // Function to unpause the contract
    function unpause() public onlyOwner {
        _unpause();
    }
}
