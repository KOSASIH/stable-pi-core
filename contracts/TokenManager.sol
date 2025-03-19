// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract TokenManager is Ownable {
    using SafeMath for uint256;

    // Mapping to store token addresses and their corresponding balances
    mapping(address => mapping(address => uint256)) private _balances; // user => token => balance
    mapping(address => bool) private _allowedTokens; // Allowed tokens for management

    event TokenAdded(address indexed token);
    event TokenRemoved(address indexed token);
    event TokensMinted(address indexed token, address indexed to, uint256 amount);
    event TokensBurned(address indexed token, address indexed from, uint256 amount);
    event TokensTransferred(address indexed token, address indexed from, address indexed to, uint256 amount);

    // Modifier to check if the token is allowed
    modifier onlyAllowedToken(address token) {
        require(_allowedTokens[token], "TokenManager: Token not allowed");
        _;
    }

    // Function to add a new token to the manager
    function addToken(address token) external onlyOwner {
        require(token != address(0), "TokenManager: Invalid token address");
        require(!_allowedTokens[token], "TokenManager: Token already added");

        _allowedTokens[token] = true;
        emit TokenAdded(token);
    }

    // Function to remove a token from the manager
    function removeToken(address token) external onlyOwner onlyAllowedToken(token) {
        delete _allowedTokens[token];
        emit TokenRemoved(token);
    }

    // Function to mint tokens to a specified address
    function mintTokens(address token, address to, uint256 amount) external onlyOwner onlyAllowedToken(token) {
        require(to != address(0), "TokenManager: Invalid recipient address");
        require(amount > 0, "TokenManager: Amount must be greater than zero");

        IERC20(token).transfer(to, amount);
        _balances[to][token] = _balances[to][token].add(amount);
        emit TokensMinted(token, to, amount);
    }

    // Function to burn tokens from a specified address
    function burnTokens(address token, address from, uint256 amount) external onlyOwner onlyAllowedToken(token) {
        require(from != address(0), "TokenManager: Invalid address");
        require(amount > 0, "TokenManager: Amount must be greater than zero");
        require(_balances[from][token] >= amount, "TokenManager: Insufficient balance");

        _balances[from][token] = _balances[from][token].sub(amount);
        emit TokensBurned(token, from, amount);
    }

    // Function to transfer tokens from one address to another
    function transferTokens(address token, address from, address to, uint256 amount) external onlyOwner onlyAllowedToken(token) {
        require(from != address(0), "TokenManager: Invalid sender address");
        require(to != address(0), "TokenManager: Invalid recipient address");
        require(amount > 0, "TokenManager: Amount must be greater than zero");
        require(_balances[from][token] >= amount, "TokenManager: Insufficient balance");

        _balances[from][token] = _balances[from][token].sub(amount);
        _balances[to][token] = _balances[to][token].add(amount);
        emit TokensTransferred(token, from, to, amount);
    }

    // Function to get the balance of a specific token for a user
    function getTokenBalance(address user, address token) external view onlyAllowedToken(token) returns (uint256) {
        return _balances[user][token];
    }

    // Function to check if a token is allowed
    function isTokenAllowed(address token) external view returns (bool) {
        return _allowedTokens[token];
    }
}
