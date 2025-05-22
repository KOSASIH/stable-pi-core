// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";

contract PiStableCoin is Ownable, Pausable {
    uint256 public constant GCV_VALUE = 314159 * 10**18; // $314,159 in wei
    uint256 public totalSupply;
    mapping(address => uint256) public balances;
    mapping(address => mapping(address => uint256)) public allowances;

    uint256 public transactionFee; // Fee percentage in basis points (10000 = 100%)
    address public feeRecipient;

    event Mint(address indexed to, uint256 amount);
    event Burn(address indexed from, uint256 amount);
    event Transfer(address indexed from, address indexed to, uint256 amount);
    event FeeUpdated(uint256 newFee);
    event FeeRecipientUpdated(address newRecipient);
    event SupplyAdjusted(uint256 oldSupply, uint256 newSupply, int256 supplyChange, uint256 marketPrice);

    modifier onlyFeeRecipient() {
        require(msg.sender == feeRecipient, "Caller is not the fee recipient");
        _;
    }

    constructor(address _feeRecipient, uint256 _transactionFee) {
        require(_feeRecipient != address(0), "Invalid fee recipient");
        require(_transactionFee <= 10000, "Fee exceeds maximum limit");
        feeRecipient = _feeRecipient;
        transactionFee = _transactionFee;
    }

    function stabilizeValue(uint256 amount) public onlyOwner whenNotPaused {
        require(amount > 0, "Amount must be greater than 0");
        totalSupply += amount;
        balances[msg.sender] += amount;
        emit Mint(msg.sender, amount);
    }

    function mint(address to, uint256 amount) public onlyOwner whenNotPaused {
        require(to != address(0), "Cannot mint to the zero address");
        require(amount > 0, "Amount must be greater than 0");

        totalSupply += amount;
        balances[to] += amount;
        emit Mint(to, amount);
    }

    function burn(uint256 amount) public whenNotPaused {
        require(amount > 0, "Amount must be greater than 0");
        require(balances[msg.sender] >= amount, "Insufficient balance");

        totalSupply -= amount;
        balances[msg.sender] -= amount;
        emit Burn(msg.sender, amount);
    }

    function transfer(address to, uint256 amount) public whenNotPaused returns (bool) {
        require(to != address(0), "Cannot transfer to the zero address");
        require(balances[msg.sender] >= amount, "Insufficient balance");

        uint256 fee = (amount * transactionFee) / 10000;
        uint256 amountAfterFee = amount - fee;

        balances[msg.sender] -= amount;
        balances[to] += amountAfterFee;
        balances[feeRecipient] += fee;

        emit Transfer(msg.sender, to, amountAfterFee);
        emit Transfer(msg.sender, feeRecipient, fee);
        return true;
    }

    function approve(address spender, uint256 amount) public whenNotPaused returns (bool) {
        allowances[msg.sender][spender] = amount;
        return true;
    }

    function transferFrom(address from, address to, uint256 amount) public whenNotPaused returns (bool) {
        require(from != address(0), "Cannot transfer from the zero address");
        require(to != address(0), "Cannot transfer to the zero address");
        require(balances[from] >= amount, "Insufficient balance");
        require(allowances[from][msg.sender] >= amount, "Allowance exceeded");

        uint256 fee = (amount * transactionFee) / 10000;
        uint256 amountAfterFee = amount - fee;

        balances[from] -= amount;
        balances[to] += amountAfterFee;
        balances[feeRecipient] += fee;

        allowances[from][msg.sender] -= amount;

        emit Transfer(from, to, amountAfterFee);
        emit Transfer(from, feeRecipient, fee);
        return true;
    }

    function setTransactionFee(uint256 newFee) public onlyOwner {
        require(newFee <= 10000, "Fee exceeds maximum limit");
        transactionFee = newFee;
        emit FeeUpdated(newFee);
    }

    function setFeeRecipient(address newRecipient) public onlyOwner {
        require(newRecipient != address(0), "Invalid fee recipient");
        feeRecipient = newRecipient;
        emit FeeRecipientUpdated(newRecipient);
    }

    function pause() public onlyOwner {
        _pause();
    }

    function unpause() public onlyOwner {
        _unpause();
    }

    function balanceOf(address account) public view returns (uint256) {
        return balances[account];
    }

    function allowance(address owner, address spender) public view returns (uint256) {
        return allowances[owner][spender];
    }

    /**
     * @notice Adjust supply based on the market price compared to the GCV_VALUE.
     *         If market price is below GCV_VALUE, burn tokens from owner to reduce supply.
     *         If market price is above GCV_VALUE, mint new tokens to owner to increase supply.
     * @param marketPrice The current market price in wei
     */
    function adjustSupply(uint256 marketPrice) public onlyOwner whenNotPaused {
        require(marketPrice > 0, "Market price must be positive");

        uint256 oldSupply = totalSupply;
        int256 supplyChange = 0;

        if (marketPrice < GCV_VALUE) {
            // Calculate difference scaled by token decimals
            uint256 diff = (GCV_VALUE - marketPrice);
            uint256 burnAmount = diff; // Already in 18-decimals wei

            // Limit burn to owner's balance to prevent underflow
            uint256 ownerBalance = balances[msg.sender];
            if (burnAmount > ownerBalance) {
                burnAmount = ownerBalance;
            }

            require(burnAmount > 0, "No tokens available to burn for supply adjustment");

            totalSupply -= burnAmount;
            balances[msg.sender] -= burnAmount;
            supplyChange = -int256(burnAmount);

            emit Burn(msg.sender, burnAmount);

        } else if (marketPrice > GCV_VALUE) {
            uint256 diff = (marketPrice - GCV_VALUE);
            uint256 mintAmount = diff; // Already in 18-decimals wei

            totalSupply += mintAmount;
            balances[msg.sender] += mintAmount;
            supplyChange = int256(mintAmount);

            emit Mint(msg.sender, mintAmount);
        }

        emit SupplyAdjusted(oldSupply, totalSupply, supplyChange, marketPrice);
    }
}
