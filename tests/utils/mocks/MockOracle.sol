// utils/mocks/MockOracle.sol

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MockOracle {
    uint256 private price;

    constructor(uint256 initialPrice) {
        price = initialPrice;
    }

    function setPrice(uint256 newPrice) external {
        price = newPrice;
    }

    function getPrice() external view returns (uint256) {
        return price;
    }
}
