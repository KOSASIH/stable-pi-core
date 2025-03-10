// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract PriceFeed is Ownable {
    using SafeMath for uint256;

    // Struct to hold price data
    struct PriceData {
        uint256 price; // Price in wei
        uint256 timestamp; // Timestamp of the price update
    }

    // Mapping of asset symbols to their price data
    mapping(string => PriceData) private prices;

    // Event emitted when a price is updated
    event PriceUpdated(string indexed asset, uint256 price, uint256 timestamp);

    /**
     * @dev Updates the price of a given asset.
     * @param asset The symbol of the asset (e.g., "ETH", "BTC").
     * @param price The new price in wei.
     */
    function updatePrice(string memory asset, uint256 price) external onlyOwner {
        require(price > 0, "Price must be greater than zero");

        prices[asset] = PriceData({
            price: price,
            timestamp: block.timestamp
        });

        emit PriceUpdated(asset, price, block.timestamp);
    }

    /**
     * @dev Retrieves the price of a given asset.
     * @param asset The symbol of the asset.
     * @return price The price in wei.
     * @return timestamp The timestamp of the last price update.
     */
    function getPrice(string memory asset) external view returns (uint256 price, uint256 timestamp) {
        PriceData memory priceData = prices[asset];
        return (priceData.price, priceData.timestamp);
    }

    /**
     * @dev Retrieves the latest price of a given asset.
     * @param asset The symbol of the asset.
     * @return price The latest price in wei.
     */
    function latestPrice(string memory asset) external view returns (uint256 price) {
        return prices[asset].price;
    }
}
