// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract PriceFeedAggregator is AccessControl {
    using SafeMath for uint256;

    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");

    // Struct to hold price feed information
    struct PriceFeed {
        AggregatorV3Interface feed;
        uint256 weight; // Weight for weighted average calculation
    }

    PriceFeed[] public priceFeeds;
    event PriceFeedAdded(address indexed feed, uint256 weight);
    event PriceFeedRemoved(address indexed feed);
    event PriceUpdated(uint256 averagePrice);

    constructor() {
        _setupRole(ADMIN_ROLE, msg.sender); // Grant admin role to contract deployer
    }

    // Function to add a new price feed
    function addPriceFeed(address _priceFeed, uint256 _weight) external onlyRole(ADMIN_ROLE) {
        require(_priceFeed != address(0), "Invalid address");
        require(_weight > 0, "Weight must be greater than zero");

        priceFeeds.push(PriceFeed({
            feed: AggregatorV3Interface(_priceFeed),
            weight: _weight
        }));

        emit PriceFeedAdded(_priceFeed, _weight);
    }

    // Function to remove a price feed
    function removePriceFeed(uint256 index) external onlyRole(ADMIN_ROLE) {
        require(index < priceFeeds.length, "Index out of bounds");

        address feedAddress = address(priceFeeds[index].feed);
        priceFeeds[index] = priceFeeds[priceFeeds.length - 1]; // Move the last element into the place to delete
        priceFeeds.pop(); // Remove the last element

        emit PriceFeedRemoved(feedAddress);
    }

    // Function to get the latest price from all price feeds
    function getLatestPrice() public view returns (uint256) {
        uint256 totalWeightedPrice = 0;
        uint256 totalWeight = 0;

        for (uint256 i = 0; i < priceFeeds.length; i++) {
            (
                ,
                int price,
                ,
                ,
            ) = priceFeeds[i].feed.latestRoundData();
            if (price > 0) {
                totalWeightedPrice = totalWeightedPrice.add(uint256(price).mul(priceFeeds[i].weight));
                totalWeight = totalWeight.add(priceFeeds[i].weight);
            }
        }

        require(totalWeight > 0, "No valid price feeds available");
        uint256 averagePrice = totalWeightedPrice.div(totalWeight);
        emit PriceUpdated(averagePrice);
        return averagePrice;
    }

    // Function to get the number of price feeds
    function getPriceFeedCount() external view returns (uint256) {
        return priceFeeds.length;
    }

    // Function to get price feed details
    function getPriceFeed(uint256 index) external view returns (address, uint256) {
        require(index < priceFeeds.length, "Index out of bounds");
        return (address(priceFeeds[index].feed), priceFeeds[index].weight);
    }
}
