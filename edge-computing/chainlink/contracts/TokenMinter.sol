// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract TokenMinter is AccessControl, Pausable {
    using SafeMath for uint256;

    // Define roles
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    bytes32 public constant ADMIN_ROLE = keccak256("ADMIN_ROLE");

    IERC20 public token; // The ERC20 token to mint
    uint256 public mintingLimit; // Maximum amount that can be minted in a single transaction

    event TokensMinted(address indexed to, uint256 amount);
    event MintingLimitUpdated(uint256 newLimit);
    event MintingPaused();
    event MintingUnpaused();

    constructor(address _token, uint256 _mintingLimit) {
        token = IERC20(_token);
        mintingLimit = _mintingLimit;

        // Grant roles to the deployer
        _setupRole(ADMIN_ROLE, msg.sender);
        _setupRole(MINTER_ROLE, msg.sender);
    }

    // Function to mint tokens
    function mintTokens(address to, uint256 amount) external onlyRole(MINTER_ROLE) whenNotPaused {
        require(amount <= mintingLimit, "Amount exceeds minting limit");
        require(to != address(0), "Cannot mint to the zero address");

        // Assuming the token contract has a mint function
        // This requires the token contract to implement a mint function
        // Uncomment the following line if the mint function exists
        // token.mint(to, amount);

        emit TokensMinted(to, amount);
    }

    // Function to update the minting limit
    function updateMintingLimit(uint256 newLimit) external onlyRole(ADMIN_ROLE) {
        mintingLimit = newLimit;
        emit MintingLimitUpdated(newLimit);
    }

    // Emergency functions to pause and unpause minting
    function pauseMinting() external onlyRole(ADMIN_ROLE) {
        _pause();
        emit MintingPaused();
    }

    function unpauseMinting() external onlyRole(ADMIN_ROLE) {
        _unpause();
        emit MintingUnpaused();
    }

    // Function to check the current minting limit
    function getMintingLimit() external view returns (uint256) {
        return mintingLimit;
    }
}
