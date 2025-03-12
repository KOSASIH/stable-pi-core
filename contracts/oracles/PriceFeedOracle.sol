// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./IPriceFeed.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";

contract PriceFeedOracle is IPriceFeed, AccessControl {
    bytes32 public constant UPDATER_ROLE = keccak256("UPDATER_ROLE");

    struct PriceData {
        uint256 price;
        uint256 timestamp;
    }

    // Mapping to store historical prices
    mapping(uint256 => PriceData) private priceHistory;
    uint256 private latestRoundId;
    uint8 private decimals;
    string private description;

    event PriceUpdated(uint256 indexed price, uint256 indexed timestamp, uint256 indexed roundId);

    constructor(uint8 _decimals, string memory _description) {
        _setupRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _setupRole(UPDATER_ROLE, msg.sender);
        decimals = _decimals;
        description = _description;
    }

    /**
     * @dev Updates the price. This function can only be called by an authorized address.
     * @param price The new price to set.
     */
    function updatePrice(uint256 price) external onlyRole(UPDATER_ROLE) {
        latestRoundId++;
        priceHistory[latestRoundId] = PriceData(price, block.timestamp);
        emit PriceUpdated(price, block.timestamp, latestRoundId);
    }

    function getLatestPrice() external view override returns (uint256 price, uint256 timestamp) {
        PriceData storage data = priceHistory[latestRoundId];
        return (data.price, data.timestamp);
    }

    function getPriceAt(uint256 roundId) external view override returns (uint256 price) {
        require(roundId > 0 && roundId <= latestRoundId, "Invalid round ID");
        return priceHistory[roundId].price;
    }

    function getDecimals() external view override returns (uint8) {
        return decimals;
    }

    function getDescription() external view override returns (string memory) {
        return description;
    }

    function getLatestRoundId() external view override returns (uint256 roundId) {
        return latestRoundId;
    }

    function getPriceByRoundId(uint256 roundId) external view override returns (uint256 price, uint256 timestamp) {
        require(roundId > 0 && roundId <= latestRoundId, "Invalid round ID");
        PriceData storage data = priceHistory[roundId];
        return (data.price, data.timestamp);
    }

    /**
     * @dev Grants the UPDATER_ROLE to an address.
     * @param account The address to grant the role to.
     */
    function grantUpdaterRole(address account) external onlyRole(DEFAULT_ADMIN_ROLE) {
        grantRole(UPDATER_ROLE, account);
    }

    /**
     * @dev Revokes the UPDATER_ROLE from an address.
     * @param account The address to revoke the role from.
     */
    function revokeUpdaterRole(address account) external onlyRole(DEFAULT_ADMIN_ROLE) {
        revokeRole(UPDATER_ROLE, account);
    }
}
