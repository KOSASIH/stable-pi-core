// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./IPriceFeed.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract AutomatedSupplyManager is AccessControl {
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant SUPPLY_ADJUSTER_ROLE = keccak256("SUPPLY_ADJUSTER_ROLE");

    IERC20 public token;
    IPriceFeed[] public priceFeeds; // Array of price feeds
    uint256 public targetPrice; // Target price for supply adjustments
    uint256 public adjustmentFactor; // Percentage adjustment (e.g., 5 for 5%)
    uint256 public lastAdjustmentTime;
    uint256 public adjustmentCooldown; // Time in seconds

    event SupplyAdjusted(uint256 newSupply, uint256 timestamp);
    event PriceFeedAdded(IPriceFeed indexed priceFeed);
    event PriceFeedRemoved(IPriceFeed indexed priceFeed);

    constructor(
        address _token,
        uint256 _targetPrice,
        uint256 _adjustmentFactor,
        uint256 _adjustmentCooldown
    ) {
        token = IERC20(_token);
        targetPrice = _targetPrice;
        adjustmentFactor = _adjustmentFactor;
        adjustmentCooldown = _adjustmentCooldown;
        lastAdjustmentTime = block.timestamp;

        _setupRole(ADMIN_ROLE, msg.sender);
        _setupRole(SUPPLY_ADJUSTER_ROLE, msg.sender);
    }

    function addPriceFeed(IPriceFeed priceFeed) external onlyRole(ADMIN_ROLE) {
        priceFeeds.push(priceFeed);
        emit PriceFeedAdded(priceFeed);
    }

    function removePriceFeed(uint256 index) external onlyRole(ADMIN_ROLE) {
        require(index < priceFeeds.length, "Index out of bounds");
        IPriceFeed removedFeed = priceFeeds[index];
        priceFeeds[index] = priceFeeds[priceFeeds.length - 1]; // Move the last element into the place to delete
        priceFeeds.pop(); // Remove the last element
        emit PriceFeedRemoved(removedFeed);
    }

    function adjustSupply() external onlyRole(SUPPLY_ADJUSTER_ROLE) {
        require(block.timestamp >= lastAdjustmentTime + adjustmentCooldown, "Cooldown period not met");

        uint256 totalPrice = 0;
        uint256 validFeeds = 0;

        for (uint256 i = 0; i < priceFeeds.length; i++) {
            (uint256 currentPrice, ) = priceFeeds[i].getLatestPrice();
            if (currentPrice > 0) {
                totalPrice += currentPrice;
                validFeeds++;
            }
        }

        require(validFeeds > 0, "No valid price feeds available");
        uint256 averagePrice = totalPrice / validFeeds;

        uint256 currentSupply = token.totalSupply();

        if (averagePrice < targetPrice) {
            uint256 adjustmentAmount = (currentSupply * adjustmentFactor) / 100;
            // Mint new tokens (assuming mint function exists in the token contract)
            // token.mint(address(this), adjustmentAmount);
            emit SupplyAdjusted(currentSupply + adjustmentAmount, block.timestamp);
        } else if (averagePrice > targetPrice) {
            uint256 adjustmentAmount = (currentSupply * adjustmentFactor) / 100;
            // Burn tokens (assuming burn function exists in the token contract)
            // token.burn(address(this), adjustmentAmount);
            emit SupplyAdjusted(currentSupply - adjustmentAmount, block.timestamp);
        }

        lastAdjustmentTime = block.timestamp;
    }

    function setTargetPrice(uint256 _targetPrice) external onlyRole(ADMIN_ROLE) {
        targetPrice = _targetPrice;
    }

    function setAdjustmentFactor(uint256 _adjustmentFactor) external onlyRole(ADMIN_ROLE) {
        adjustmentFactor = _adjustmentFactor;
    }

    function setAdjustmentCooldown(uint256 _adjustmentCooldown) external onlyRole(ADMIN_ROLE) {
        adjustmentCooldown = _adjustmentCooldown;
    }

    function getPriceFeeds() external view returns (IPriceFeed[] memory) {
        return priceFeeds;
    }
}
