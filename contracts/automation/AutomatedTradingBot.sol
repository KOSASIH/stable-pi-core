// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

interface IPriceOracle {
    function getLatestPrice() external view returns (uint256);
}

contract AutomatedTradingBot is AccessControl {
    using SafeMath for uint256;

    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");
    bytes32 public constant TRADER_ROLE = keccak256("TRADER_ROLE");

    IERC20 public token;
    IPriceOracle public priceOracle;
    uint256 public stopLossPercentage; // e.g., 5 for 5%
    uint256 public takeProfitPercentage; // e.g., 10 for 10%
    uint256 public lastTradePrice;

    event TradeExecuted(address indexed trader, uint256 amount, string action);
    event ParametersUpdated(uint256 stopLoss, uint256 takeProfit);

    constructor(address _token, address _priceOracle) {
        token = IERC20(_token);
        priceOracle = IPriceOracle(_priceOracle);
        _setupRole(ADMIN_ROLE, msg.sender);
        _setupRole(TRADER_ROLE, msg.sender);
    }

    function setTradingParameters(uint256 _stopLossPercentage, uint256 _takeProfitPercentage) external onlyRole(ADMIN_ROLE) {
        stopLossPercentage = _stopLossPercentage;
        takeProfitPercentage = _takeProfitPercentage;
        emit ParametersUpdated(stopLossPercentage, takeProfitPercentage);
    }

    function executeTrade(uint256 amount, string memory action) external onlyRole(TRADER_ROLE) {
        require(amount > 0, "Amount must be greater than zero");
        uint256 currentPrice = priceOracle.getLatestPrice();

        if (keccak256(abi.encodePacked(action)) == keccak256("buy")) {
            require(token.balanceOf(address(this)) >= amount, "Insufficient balance to buy");
            lastTradePrice = currentPrice;
            // Logic to buy tokens
            emit TradeExecuted(msg.sender, amount, "buy");
        } else if (keccak256(abi.encodePacked(action)) == keccak256("sell")) {
            require(token.balanceOf(msg.sender) >= amount, "Insufficient balance to sell");
            lastTradePrice = currentPrice;
            // Logic to sell tokens
            emit TradeExecuted(msg.sender, amount, "sell");
        } else {
            revert("Invalid action");
        }

        manageRisk(currentPrice);
    }

    function manageRisk(uint256 currentPrice) internal {
        uint256 stopLossPrice = lastTradePrice.mul(100 - stopLossPercentage).div(100);
        uint256 takeProfitPrice = lastTradePrice.mul(100 + takeProfitPercentage).div(100);

        if (currentPrice <= stopLossPrice) {
            // Logic to execute stop-loss
            emit TradeExecuted(msg.sender, token.balanceOf(msg.sender), "stop-loss");
        } else if (currentPrice >= takeProfitPrice) {
            // Logic to execute take-profit
            emit TradeExecuted(msg.sender, token.balanceOf(msg.sender), "take-profit");
        }
    }

    function withdrawTokens(uint256 amount) external onlyRole(ADMIN_ROLE) {
        require(token.balanceOf(address(this)) >= amount, "Insufficient balance to withdraw");
        token.transfer(msg.sender, amount);
    }
}
