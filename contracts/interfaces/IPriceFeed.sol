// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IPriceFeed {
    /**
     * @dev Emitted when the price is updated.
     * @param price The new price.
     * @param timestamp The timestamp of the price update.
     */
    event PriceUpdated(uint256 indexed price, uint256 indexed timestamp);

    /**
     * @dev Gets the latest price from the price feed.
     * @return price The latest price.
     * @return timestamp The timestamp of the latest price.
     */
    function getLatestPrice() external view returns (uint256 price, uint256 timestamp);

    /**
     * @dev Gets the price at a specific timestamp.
     * @param timestamp The timestamp for which to retrieve the price.
     * @return price The price at the specified timestamp.
     */
    function getPriceAt(uint256 timestamp) external view returns (uint256 price);

    /**
     * @dev Gets the price feed's decimals.
     * @return decimals The number of decimals used by the price feed.
     */
    function getDecimals() external view returns (uint8 decimals);

    /**
     * @dev Gets the price feed's description.
     * @return description A string describing the price feed.
     */
    function getDescription() external view returns (string memory description);

    /**
     * @dev Gets the latest round ID for the price feed.
     * @return roundId The latest round ID.
     */
    function getLatestRoundId() external view returns (uint256 roundId);

    /**
     * @dev Gets the price and timestamp for a specific round ID.
     * @param roundId The round ID for which to retrieve the price.
     * @return price The price at the specified round ID.
     * @return timestamp The timestamp of the price at the specified round ID.
     */
    function getPriceByRoundId(uint256 roundId) external view returns (uint256 price, uint256 timestamp);
}
