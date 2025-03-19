// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "./IPriceFeed.sol";
import "./SafeMath.sol";

contract PiCoinDynamicPegging is AccessControl {
    using SafeMath for uint256;

    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant SUPPLY_MANAGER_ROLE = keccak256("SUPPLY_MANAGER_ROLE");

    IERC20 public piCoin; // The PiCoin token
    IPriceFeed public priceFeed; // Price feed for market price
    uint256 public constant TARGET_PEG = 314159 * 10**18; // Target peg value in wei (assuming 18 decimals)
    uint256 public adjustmentFactor; // Percentage adjustment factor (e.g., 5 for 5%)
    uint256 public lastAdjustmentTime;
    uint256 public adjustmentCooldown; // Time in seconds

    event PegAdjusted(uint256 newSupply, uint256 timestamp);
    event AdjustmentFactorUpdated(uint256 newAdjustmentFactor);

    constructor(
        address _piCoin,
        address _priceFeed,
        uint256 _adjustmentFactor,
        uint256 _adjustmentCooldown
    ) {
        piCoin = IERC20(_piCoin);
        priceFeed = IPriceFeed(_priceFeed);
        adjustmentFactor = _adjustmentFactor;
        adjustmentCooldown = _adjustmentCooldown;
        lastAdjustmentTime = block.timestamp;

        _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _setupRole(SUPPLY_MANAGER_ROLE, msg.sender);
    }

    function adjustPeg() external onlyRole(SUPPLY_MANAGER_ROLE) {
        require(block.timestamp >= lastAdjustmentTime + adjustmentCooldown, "Cooldown period not met");

        (uint256 currentPrice, ) = priceFeed.getLatestPrice();
        uint256 currentSupply = piCoin.totalSupply();

        if (currentPrice < TARGET_PEG) {
            uint256 adjustmentAmount = (currentSupply.mul(adjustmentFactor)).div(100);
            // Mint new tokens (assuming mint function exists in the token contract)
            // piCoin.mint(address(this), adjustmentAmount);
            emit PegAdjusted(currentSupply.add(adjustmentAmount), block.timestamp);
        } else if (currentPrice > TARGET_PEG) {
            uint256 adjustmentAmount = (currentSupply.mul(adjustmentFactor)).div(100);
            // Burn tokens (assuming burn function exists in the token contract)
            // piCoin.burn(address(this), adjustmentAmount);
            emit PegAdjusted(currentSupply.sub(adjustmentAmount), block.timestamp);
        }

        lastAdjustmentTime = block.timestamp;
    }

    function setAdjustmentFactor(uint256 _adjustmentFactor) external onlyRole(ADMIN_ROLE) {
        adjustmentFactor = _adjustmentFactor;
        emit AdjustmentFactorUpdated(_adjustmentFactor);
    }

    function setAdjustmentCooldown(uint256 _adjustmentCooldown) external onlyRole(ADMIN_ROLE) {
        adjustmentCooldown = _adjustmentCooldown;
    }

    function getCurrentPrice() external view returns (uint256) {
        return priceFeed.getLatestPrice();
    }
}
