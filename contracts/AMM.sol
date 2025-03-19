// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract AMM is Ownable, ReentrancyGuard {
    using SafeMath for uint256;

    IERC20 public tokenA;
    IERC20 public tokenB;

    uint256 public reserveA; // Amount of Token A in the pool
    uint256 public reserveB; // Amount of Token B in the pool
    uint256 public tradingFee = 30; // 0.3% fee (30 basis points)
    uint256 public constant FEE_DENOMINATOR = 10000;

    event LiquidityAdded(address indexed provider, uint256 amountA, uint256 amountB);
    event LiquidityRemoved(address indexed provider, uint256 amountA, uint256 amountB);
    event TokensSwapped(address indexed user, address indexed inputToken, uint256 inputAmount, uint256 outputAmount);
    event FlashLoan(address indexed borrower, address indexed token, uint256 amount);

    constructor(address _tokenA, address _tokenB) {
        tokenA = IERC20(_tokenA);
        tokenB = IERC20(_tokenB);
    }

    // Add liquidity to the pool
    function addLiquidity(uint256 amountA, uint256 amountB) external nonReentrant {
        require(amountA > 0 && amountB > 0, "Invalid amounts");

        // Transfer tokens from the user to the contract
        tokenA.transferFrom(msg.sender, address(this), amountA);
        tokenB.transferFrom(msg.sender, address(this), amountB);

        // Update reserves
        reserveA = reserveA.add(amountA);
        reserveB = reserveB.add(amountB);

        emit LiquidityAdded(msg.sender, amountA, amountB);
    }

    // Remove liquidity from the pool
    function removeLiquidity(uint256 amountA, uint256 amountB) external nonReentrant {
        require(amountA > 0 && amountB > 0, "Invalid amounts");
        require(reserveA >= amountA && reserveB >= amountB, "Insufficient reserves");

        // Update reserves
        reserveA = reserveA.sub(amountA);
        reserveB = reserveB.sub(amountB);

        // Transfer tokens back to the user
        tokenA.transfer(msg.sender, amountA);
        tokenB.transfer(msg.sender, amountB);

        emit LiquidityRemoved(msg.sender, amountA, amountB);
    }

    // Swap Token A for Token B
    function swapAForB(uint256 amountA) external nonReentrant {
        require(amountA > 0, "Invalid amount");
        require(reserveA >= amountA, "Insufficient reserve A");

        // Calculate amount of Token B to send back
        uint256 amountB = getAmountOut(amountA, reserveA, reserveB);
        require(amountB > 0, "Insufficient output amount");

        // Update reserves
        reserveA = reserveA.add(amountA);
        reserveB = reserveB.sub(amountB);

        // Transfer Token A from user and Token B to user
        tokenA.transferFrom(msg.sender, address(this), amountA);
        tokenB.transfer(msg.sender, amountB);

        emit TokensSwapped(msg.sender, address(tokenA), amountA, amountB);
    }

    // Swap Token B for Token A
    function swapBForA(uint256 amountB) external nonReentrant {
        require(amountB > 0, "Invalid amount");
        require(reserveB >= amountB, "Insufficient reserve B");

        // Calculate amount of Token A to send back
        uint256 amountA = getAmountOut(amountB, reserveB, reserveA);
        require(amountA > 0, "Insufficient output amount");

        // Update reserves
        reserveB = reserveB.add(amountB);
        reserveA = reserveA.sub(amountA);

        // Transfer Token B from user and Token A to user
        tokenB.transferFrom(msg.sender, address(this), amountB);
        tokenA.transfer(msg.sender, amountA);

        emit TokensSwapped(msg.sender, address(token B), amountB, amountA);
    }

    // Calculate output amount based on the constant product formula
    function getAmountOut(uint256 inputAmount, uint256 inputReserve, uint256 outputReserve) internal view returns (uint256) {
        require(inputReserve > 0 && outputReserve > 0, "Invalid reserves");
        require(inputAmount > 0, "Invalid input amount");

        uint256 inputAmountWithFee = inputAmount.mul(FEE_DENOMINATOR.sub(tradingFee));
        uint256 numerator = inputAmountWithFee.mul(outputReserve);
        uint256 denominator = inputReserve.mul(FEE_DENOMINATOR).add(inputAmountWithFee);
        return numerator / denominator;
    }

    // Flash loan functionality
    function flashLoan(address token, uint256 amount) external nonReentrant {
        require(amount > 0, "Invalid amount");
        IERC20(token).transfer(msg.sender, amount);
        emit FlashLoan(msg.sender, token, amount);
    }

    // Repay flash loan
    function repayFlashLoan(address token, uint256 amount) external {
        require(amount > 0, "Invalid amount");
        IERC20(token).transferFrom(msg.sender, address(this), amount);
    }

    // Get reserves
    function getReserves() external view returns (uint256, uint256) {
        return (reserveA, reserveB);
    }

    // Update trading fee
    function updateTradingFee(uint256 newFee) external onlyOwner {
        require(newFee < FEE_DENOMINATOR, "Invalid fee");
        tradingFee = newFee;
    }
}
