// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title IAMM
 * @dev Interface for an Automated Market Maker (AMM).
 */
interface IAMM {
    
    /**
     * @dev Emitted when liquidity is added to the AMM.
     * @param provider The address of the liquidity provider.
     * @param tokenA The address of the first token.
     * @param tokenB The address of the second token.
     * @param amountA The amount of the first token added.
     * @param amountB The amount of the second token added.
     */
    event LiquidityAdded(address indexed provider, address indexed tokenA, address indexed tokenB, uint256 amountA, uint256 amountB);

    /**
     * @dev Emitted when liquidity is removed from the AMM.
     * @param provider The address of the liquidity provider.
     * @param tokenA The address of the first token.
     * @param tokenB The address of the second token.
     * @param amountA The amount of the first token removed.
     * @param amountB The amount of the second token removed.
     */
    event LiquidityRemoved(address indexed provider, address indexed tokenA, address indexed tokenB, uint256 amountA, uint256 amountB);

    /**
     * @dev Emitted when a swap occurs.
     * @param user The address of the user performing the swap.
     * @param tokenIn The address of the token being swapped in.
     * @param tokenOut The address of the token being swapped out.
     * @param amountIn The amount of the token being swapped in.
     * @param amountOut The amount of the token being swapped out.
     */
    event SwapExecuted(address indexed user, address indexed tokenIn, address indexed tokenOut, uint256 amountIn, uint256 amountOut);

    /**
     * @dev Add liquidity to the AMM.
     * @param tokenA The address of the first token.
     * @param tokenB The address of the second token.
     * @param amountA The amount of the first token to add.
     * @param amountB The amount of the second token to add.
     * @return liquidity The amount of liquidity tokens minted.
     */
    function addLiquidity(address tokenA, address tokenB, uint256 amountA, uint256 amountB) external returns (uint256 liquidity);

    /**
     * @dev Remove liquidity from the AMM.
     * @param tokenA The address of the first token.
     * @param tokenB The address of the second token.
     * @param liquidity The amount of liquidity tokens to burn.
     * @return amountA The amount of the first token returned.
     * @return amountB The amount of the second token returned.
     */
    function removeLiquidity(address tokenA, address tokenB, uint256 liquidity) external returns (uint256 amountA, uint256 amountB);

    /**
     * @dev Swap one token for another.
     * @param tokenIn The address of the token being swapped in.
     * @param tokenOut The address of the token being swapped out.
     * @param amountIn The amount of the token being swapped in.
     * @return amountOut The amount of the token being swapped out.
     */
    function swap(address tokenIn, address tokenOut, uint256 amountIn) external returns (uint256 amountOut);

    /**
     * @dev Get the current price of a token pair.
     * @param tokenA The address of the first token.
     * @param tokenB The address of the second token.
     * @return price The current price of tokenA in terms of tokenB.
     */
    function getPrice(address tokenA, address tokenB) external view returns (uint256 price);

    /**
     * @dev Get the reserves of a token pair.
     * @param tokenA The address of the first token.
     * @param tokenB The address of the second token.
     * @return reserveA The reserve of the first token.
     * @return reserveB The reserve of the second token.
     */
    function getReserves(address tokenA, address tokenB) external view returns (uint256 reserveA, uint256 reserveB);
}
