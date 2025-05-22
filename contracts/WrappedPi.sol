// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/draft-ERC20Permit.sol";

/// @title WrappedPi - An advanced wrapped token for Pi network
/// @notice This contract implements a wrapped token with minting, burning, pausing, permit, and ownership control with security and extensibility in mind
contract WrappedPi is ERC20, Ownable, Pausable, ERC20Burnable, ERC20Permit {

    uint256 private _cap;

    event CapUpdated(uint256 oldCap, uint256 newCap);

    /// @notice Constructor sets the token name, symbol, cap and initializes ERC20Permit
    /// @param cap_ Max cap for total supply (use 0 for no cap)
    constructor(uint256 cap_) ERC20("Wrapped Pi", "wPI") ERC20Permit("Wrapped Pi") {
        _cap = cap_;
    }

    /// @notice Mint new tokens, callable only by owner, subject to cap and pausable
    /// @param to Receiver address
    /// @param amount Amount to mint
    function mint(address to, uint256 amount) public onlyOwner whenNotPaused {
        require(to != address(0), "WrappedPi: mint to zero address");
        if (_cap > 0) {
            require(totalSupply() + amount <= _cap, "WrappedPi: cap exceeded");
        }
        _mint(to, amount);
    }

    /// @notice Burn tokens from sender, pausable
    /// @param amount Amount to burn
    function burn(uint256 amount) public override whenNotPaused {
        super.burn(amount);
    }

    /// @notice Burn tokens from allowance, pausable
    /// @param account Account whose tokens will be burned
    /// @param amount Amount to burn
    function burnFrom(address account, uint256 amount) public override whenNotPaused {
        super.burnFrom(account, amount);
    }

    /// @notice Pause all token transfers and mint/burn functions; onlyOwner
    function pause() external onlyOwner {
        _pause();
    }

    /// @notice Unpause all token transfers and mint/burn functions; onlyOwner
    function unpause() external onlyOwner {
        _unpause();
    }

    /// @notice Update token supply cap; onlyOwner
    /// @param newCap New supply cap (0 for no cap)
    function setCap(uint256 newCap) external onlyOwner {
        require(newCap == 0 || newCap >= totalSupply(), "WrappedPi: new cap below supply");
        uint256 oldCap = _cap;
        _cap = newCap;
        emit CapUpdated(oldCap, newCap);
    }

    /// @notice Returns current supply cap (0 means no cap)
    function cap() public view returns (uint256) {
        return _cap;
    }

    /// @dev Override _beforeTokenTransfer to respect pause functionality
    function _beforeTokenTransfer(address from, address to, uint256 amount) internal override {
        super._beforeTokenTransfer(from, to, amount);
        require(!paused(), "WrappedPi: token transfer while paused");
    }
}
