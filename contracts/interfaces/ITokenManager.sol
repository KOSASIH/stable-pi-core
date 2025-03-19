// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title ITokenManager
 * @dev Interface for managing tokens in a DeFi protocol.
 */
interface ITokenManager {
    
    /**
     * @dev Emitted when a new token is created.
     * @param token The address of the newly created token.
     * @param name The name of the token.
     * @param symbol The symbol of the token.
     * @param totalSupply The total supply of the token.
     */
    event TokenCreated(address indexed token, string name, string symbol, uint256 totalSupply);

    /**
     * @dev Emitted when tokens are burned.
     * @param token The address of the token being burned.
     * @param amount The amount of tokens burned.
     * @param user The address of the user who burned the tokens.
     */
    event TokensBurned(address indexed token, uint256 amount, address indexed user);

    /**
     * @dev Emitted when tokens are transferred.
     * @param token The address of the token being transferred.
     * @param from The address of the sender.
     * @param to The address of the recipient.
     * @param amount The amount of tokens transferred.
     */
    event TokensTransferred(address indexed token, address indexed from, address indexed to, uint256 amount);

    /**
     * @dev Emitted when approval is granted for token spending.
     * @param token The address of the token.
     * @param owner The address of the token owner.
     * @param spender The address of the spender.
     * @param amount The amount approved for spending.
     */
    event ApprovalGranted(address indexed token, address indexed owner, address indexed spender, uint256 amount);

    /**
     * @dev Create a new token.
     * @param name The name of the token.
     * @param symbol The symbol of the token.
     * @param totalSupply The total supply of the token.
     * @return token The address of the newly created token.
     */
    function createToken(string calldata name, string calldata symbol, uint256 totalSupply) external returns (address token);

    /**
     * @dev Burn a specified amount of tokens.
     * @param token The address of the token to burn.
     * @param amount The amount of tokens to burn.
     */
    function burnTokens(address token, uint256 amount) external;

    /**
     * @dev Transfer tokens from one address to another.
     * @param token The address of the token to transfer.
     * @param to The address of the recipient.
     * @param amount The amount of tokens to transfer.
     */
    function transferTokens(address token, address to, uint256 amount) external;

    /**
     * @dev Approve a spender to spend a specified amount of tokens on behalf of the owner.
     * @param token The address of the token.
     * @param spender The address of the spender.
     * @param amount The amount of tokens to approve.
     */
    function approve(address token, address spender, uint256 amount) external;

    /**
     * @dev Get the balance of a specific address for a given token.
     * @param token The address of the token.
     * @param user The address of the user.
     * @return balance The balance of the user for the specified token.
     */
    function getBalance(address token, address user) external view returns (uint256 balance);

    /**
     * @dev Get the allowance of a spender for a specific token.
     * @param token The address of the token.
     * @param owner The address of the token owner.
     * @param spender The address of the spender.
     * @return allowance The amount of tokens allowed to be spent by the spender.
     */
    function allowance(address token, address owner, address spender) external view returns (uint256 allowance);
}
