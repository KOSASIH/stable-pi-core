// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract PiConverter is Ownable, Pausable {
    using SafeMath for uint256;

    mapping(address => uint256) public balances;
    uint256 public conversionRate; // Conversion rate from GCV to market price
    uint256 public feePercentage; // Fee percentage for conversions
    address public feeCollector; // Address to collect fees

    event Deposited(address indexed user, uint256 amount);
    event Converted(address indexed user, uint256 amount, uint256 convertedAmount, uint256 fee);
    event ConversionRateUpdated(uint256 newRate);
    event FeePercentageUpdated(uint256 newFeePercentage);
    event FeeCollectorUpdated(address newFeeCollector);

    constructor(uint256 initialRate, uint256 initialFeePercentage, address initialFeeCollector) {
        conversionRate = initialRate; // Set initial conversion rate
        feePercentage = initialFeePercentage; // Set initial fee percentage
        feeCollector = initialFeeCollector; // Set initial fee collector
    }

    // Function to deposit Pi Coin into the contract
    function deposit(uint256 amount) public whenNotPaused {
        require(amount > 0, "Amount must be greater than zero");
        balances[msg.sender] = balances[msg.sender].add(amount);
        emit Deposited(msg.sender, amount);
    }

    // Function to convert Pi Coin to market price
    function convert(uint256 amount) public whenNotPaused {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        uint256 convertedAmount = amount.mul(conversionRate); // Calculate converted amount
        uint256 fee = convertedAmount.mul(feePercentage).div(100); // Calculate fee
        uint256 netAmount = convertedAmount.sub(fee); // Net amount after fee

        balances[msg.sender] = balances[msg.sender].sub(amount); // Deduct the amount from user's balance
        payable(feeCollector).transfer(fee); // Transfer fee to fee collector

        emit Converted(msg.sender, amount, netAmount, fee);
    }

    // Function to update the conversion rate
    function updateConversionRate(uint256 newRate) public onlyOwner {
        conversionRate = newRate;
        emit ConversionRateUpdated(newRate);
    }

    // Function to update the fee percentage
    function updateFeePercentage(uint256 newFeePercentage) public onlyOwner {
        feePercentage = newFeePercentage;
        emit FeePercentageUpdated(newFeePercentage);
    }

    // Function to update the fee collector address
    function updateFeeCollector(address newFeeCollector) public onlyOwner {
        feeCollector = newFeeCollector;
        emit FeeCollectorUpdated(newFeeCollector);
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
