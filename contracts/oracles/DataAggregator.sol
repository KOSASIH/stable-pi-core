// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./IPriceFeed.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";

contract DataAggregator is AccessControl {
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant PRICE_FEED_ADDER_ROLE = keccak256("PRICE_FEED_ADDER_ROLE");

    IPriceFeed[] public priceFeeds;

    event PriceFeedAdded(IPriceFeed indexed priceFeed);
    event PriceAggregated(uint256 indexed aggregatedPrice, uint256 indexed timestamp);

    constructor() {
        _setupRole(ADMIN_ROLE, msg.sender);
        _setupRole(PRICE_FEED_ADDER_ROLE, msg.sender);
    }

    /**
     * @dev Adds a new price feed to the aggregator.
     * @param priceFeed The address of the price feed contract to add.
     */
    function addPriceFeed(IPriceFeed priceFeed) external onlyRole(PRICE_FEED_ADDER_ROLE) {
        priceFeeds.push(priceFeed);
        emit PriceFeedAdded(priceFeed);
    }

    /**
     * @dev Aggregates the latest prices from all registered price feeds.
     * @return aggregatedPrice The aggregated price.
     * @return timestamp The timestamp of the aggregation.
     */
    function aggregatePrices() external returns (uint256 aggregatedPrice, uint256 timestamp) {
        uint256 totalPrice = 0;
        uint256 validFeeds = 0;

        for (uint256 i = 0; i < priceFeeds.length; i++) {
            (uint256 price, uint256 feedTimestamp) = priceFeeds[i].getLatestPrice();
            if (price > 0) {
                totalPrice += price;
                validFeeds++;
                timestamp = feedTimestamp; // Use the latest timestamp from valid feeds
            }
        }

        require(validFeeds > 0, "No valid price feeds available");
        aggregatedPrice = totalPrice / validFeeds;

        emit PriceAggregated(aggregatedPrice, timestamp);
    }

    /**
     * @dev Gets the number of registered price feeds.
     * @return count The number of registered price feeds.
     */
    function getPriceFeedCount() external view returns (uint256 count) {
        return priceFeeds.length;
    }

    /**
     * @dev Gets the price feed at a specific index.
     * @param index The index of the price feed.
     * @return priceFeed The price feed contract at the specified index.
     */
    function getPriceFeed(uint256 index) external view returns (IPriceFeed priceFeed) {
        require(index < priceFeeds.length, "Index out of bounds");
        return priceFeeds[index];
    }

    /**
     * @dev Removes a price feed from the aggregator.
     * @param index The index of the price feed to remove.
     */
    function removePriceFeed(uint256 index) external onlyRole(ADMIN_ROLE) {
        require(index < priceFeeds.length, "Index out of bounds");
        priceFeeds[index] = priceFeeds[priceFeeds.length - 1]; // Move the last element into the place to delete
        priceFeeds.pop(); // Remove the last element
    }
}
