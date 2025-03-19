// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract PriceFeed is AccessControl, Pausable {
    using SafeMath for uint256;

    // Struct to hold price data
    struct PriceData {
        uint256 price; // Price in wei
        uint256 timestamp; // Timestamp of the price update
        uint256 weight; // Weight of the price source
    }

    // Mapping of asset symbols to their price data
    mapping(string => PriceData[]) private prices; // Array of price data for each asset

    // Events emitted when a price is updated
    event PriceUpdated(string indexed asset, uint256 price, uint256 timestamp);
    event PriceFeedPaused();
    event PriceFeedUnpaused();
    event GovernanceProposal(string indexed proposalType, string asset, uint256 newValue);
    event GovernanceVote(string indexed asset, address indexed voter, bool support);

    // Role definitions
    bytes32 public constant UPDATER_ROLE = keccak256("UPDATER_ROLE");
    bytes32 public constant GOVERNANCE_ROLE = keccak256("GOVERNANCE_ROLE");

    // Price change threshold
    uint256 public priceChangeThreshold;

    constructor(uint256 _priceChangeThreshold) {
        _setupRole(DEFAULT_ADMIN_ROLE, msg.sender); // Grant admin role to the contract deployer
        _setupRole(UPDATER_ROLE, msg.sender); // Grant updater role to the contract deployer
        _setupRole(GOVERNANCE_ROLE, msg.sender); // Grant governance role to the contract deployer
        priceChangeThreshold = _priceChangeThreshold; // Set the price change threshold
    }

    /**
     * @dev Updates the price of a given asset.
     * @param asset The symbol of the asset (e.g., "ETH", "BTC").
     * @param price The new price in wei.
     * @param weight The weight of the price source.
     */
    function updatePrice(string memory asset, uint256 price, uint256 weight) external onlyRole(UPDATER_ROLE) whenNotPaused {
        require(price > 0, "Price must be greater than zero");
        require(weight > 0, "Weight must be greater than zero");

        // Check if the price change exceeds the threshold
        if (prices[asset].length > 0) {
            uint256 lastPrice = prices[asset][prices[asset].length - 1].price;
            require(
                (price > lastPrice && price.sub(lastPrice) >= priceChangeThreshold) ||
                (lastPrice > price && lastPrice.sub(price) >= priceChangeThreshold),
                "Price change is below the threshold"
            );
        }

        prices[asset].push(PriceData({
            price: price,
            timestamp: block.timestamp,
            weight: weight
        }));

        emit PriceUpdated(asset, price, block.timestamp);
    }

    /**
     * @dev Retrieves the price of a given asset as a weighted average.
     * @param asset The symbol of the asset.
     * @return price The weighted average price in wei.
     * @return timestamp The timestamp of the last price update.
     */
    function getPrice(string memory asset) external view returns (uint256 price, uint256 timestamp) {
        PriceData[] memory priceDataArray = prices[asset];
        require(priceDataArray.length > 0, "No price data available");

        uint256 totalWeightedPrice = 0;
        uint256 totalWeight = 0;

        for (uint256 i = 0; i < priceDataArray.length; i++) {
            totalWeightedPrice = totalWeightedPrice.add(priceDataArray[i].price.mul(priceDataArray[i].weight));
            totalWeight = totalWeight.add(priceDataArray[i].weight);
        }

        price = totalWeightedPrice.div(totalWeight);
        timestamp = priceDataArray[priceDataArray.length - 1].timestamp;
    }

    /**
     * @dev Retrieves the latest price of a given asset.
     * @param asset The symbol of the asset.
     * @return price The latest price in wei.
     */
    function latestPrice(string memory asset) external view returns (uint256 price) {
        return prices[asset][prices[asset].length - 1].price;
    }

    /**
     * @dev Pauses the price feed, preventing updates.
     */
    function pause() external onlyRole(DEFAULT_ADMIN_ROLE) {
        _pause();
        emit PriceFeedPaused();
    }

    /**
     * @dev Unpauses the price feed, allowing updates.
     */
    function unpause() external onlyRole(DEFAULT_ADMIN_ROLE) {
        _unpause();
        emit PriceFeedUnpaused();
    }

    /**
     * @dev Proposes a new price change threshold.
     * @param newThreshold The new price change threshold.
     */
    function proposePriceChangeThreshold(uint256 newThreshold) external onlyRole(GOVERNANCE_ROLE) {
        priceChangeThreshold = newThreshold;
        emit GovernanceProposal("PriceChangeThreshold", "", newThreshold);
    }

    /**
     * @dev Casts a vote on a governance proposal.
     * @param asset The asset being voted on.
     * @param support Whether the voter supports the proposal.
     */
    function vote(string memory asset, bool support) external onlyRole(GOVERNANCE_ROLE) {
        emit GovernanceVote(asset , msg.sender, support);
    }
}
