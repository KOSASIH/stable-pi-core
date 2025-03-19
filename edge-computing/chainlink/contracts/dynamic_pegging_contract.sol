// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract DynamicPegging is AccessControl, Pausable {
    using SafeMath for uint256;

    // State variables
    IERC20 public stablecoin; // The stablecoin to be pegged
    AggregatorV3Interface[] internal priceFeeds; // Array of Chainlink price feeds
    uint256 public targetPrice; // Target price for the stablecoin
    uint256 public adjustmentFactor; // Factor to adjust supply
    uint256 public lastAdjustmentTime; // Timestamp of the last adjustment
    uint256 public adjustmentCooldown; // Cooldown period between adjustments
    uint256 public priceDeviationThreshold; // Threshold for price deviation

    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant GOVERNANCE_ROLE = keccak256("GOVERNANCE_ROLE");

    event SupplyAdjusted(uint256 newSupply);
    event PriceUpdated(uint256 newPrice);
    event AdjustmentCooldownUpdated(uint256 newCooldown);
    event PriceDeviationThresholdUpdated(uint256 newThreshold);
    event EmergencyPaused();
    event EmergencyUnpaused();

    constructor(
        address _stablecoin,
        address[] memory _priceFeeds,
        uint256 _targetPrice,
        uint256 _adjustmentFactor,
        uint256 _adjustmentCooldown,
        uint256 _priceDeviationThreshold
    ) {
        stablecoin = IERC20(_stablecoin);
        for (uint256 i = 0; i < _priceFeeds.length; i++) {
            priceFeeds.push(AggregatorV3Interface(_priceFeeds[i]));
        }
        targetPrice = _targetPrice;
        adjustmentFactor = _adjustmentFactor;
        adjustmentCooldown = _adjustmentCooldown;
        priceDeviationThreshold = _priceDeviationThreshold;
        lastAdjustmentTime = block.timestamp;

        _setupRole(ADMIN_ROLE, msg.sender);
        _setupRole(GOVERNANCE_ROLE, msg.sender);
    }

    // Function to get the latest price from the Chainlink price feeds
    function getLatestPrice() public view returns (uint256) {
        uint256 totalPrice = 0;
        uint256 validFeeds = 0;

        for (uint256 i = 0; i < priceFeeds.length; i++) {
            (
                ,
                int price,
                ,
                ,
            ) = priceFeeds[i].latestRoundData();
            if (price > 0) {
                totalPrice = totalPrice.add(uint256(price));
                validFeeds++;
            }
        }

        require(validFeeds > 0, "No valid price feeds available");
        return totalPrice.div(validFeeds);
    }

    // Function to adjust the supply of the stablecoin based on the current price
    function adjustSupply() external onlyRole(ADMIN_ROLE) whenNotPaused {
        require(block.timestamp >= lastAdjustmentTime + adjustmentCooldown, "Cooldown period not met");

        uint256 currentPrice = getLatestPrice();
        uint256 currentSupply = stablecoin.totalSupply();

        // Calculate price deviation
        uint256 priceDeviation = (currentPrice > targetPrice) ? currentPrice.sub(targetPrice) : targetPrice.sub(currentPrice);

        // Adjust supply based on price deviation
        if (priceDeviation > priceDeviationThreshold) {
            uint256 adjustmentAmount = (currentSupply.mul(adjustmentFactor)).div(100);
            if (currentPrice < targetPrice) {
                stablecoin.mint(address(this), adjustmentAmount); // Mint new tokens
                emit SupplyAdjusted(currentSupply.add(adjustmentAmount));
            } else {
                stablecoin.burn(address(this), adjustmentAmount); // Burn tokens
                emit SupplyAdjusted(currentSupply.sub(adjustmentAmount));
            }
            lastAdjustmentTime = block.timestamp;
        }

        emit PriceUpdated(currentPrice);
    }

    // Governance functions
    function proposeTargetPrice(uint256 _targetPrice) external onlyRole(GOVERNANCE_ROLE) {
        targetPrice = _targetPrice;
    }

    function proposeAdjustmentFactor(uint256 _adjustmentFactor) external onlyRole(GOVERNANCE_ROLE) {
        adjustmentFactor = _adjustmentFactor;
    }

    function proposeAdjustmentCooldown(uint256 _adjustmentCooldown) external onlyRole(GOVERNANCE_ROLE) {
        adjustmentCooldown = _adjustmentCooldown;
        emit AdjustmentCooldownUpdated(_adjustmentCooldown);
    }

    function proposePriceDeviationThreshold(uint256 _priceDeviationThreshold) external onlyRole(GOVERNANCE_ROLE) {
        priceDeviationThreshold = _priceDeviationThreshold;
        emit PriceDeviationThresholdUpdated(_priceDeviationThreshold);
    }

    // Emergency functions
    function pause() external onlyRole(ADMIN_ROLE) {
        _pause();
        emit EmergencyPaused();
    }

    function unpause() external onlyRole(ADMIN_ROLE) {
        _unpause();
        emit EmergencyUnpaused();
    }
}
