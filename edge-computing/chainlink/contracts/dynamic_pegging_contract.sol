// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract DynamicPegging is Ownable {
    using SafeMath for uint256;

    // The token that will be pegged (Pi Coin)
    IERC20 public peggedToken;

    // Price oracle address
    address public priceOracle;

    // Target price for pegging (in wei, $314159.00)
    uint256 public targetPrice = 314159 * 10**18; // Assuming 18 decimals for the token

    // Minting and burning thresholds
    uint256 public mintThreshold; // Price below which tokens are minted
    uint256 public burnThreshold; // Price above which tokens are burned

    // Event emitted when tokens are minted
    event TokensMinted(address indexed to, uint256 amount);

    // Event emitted when tokens are burned
    event TokensBurned(address indexed from, uint256 amount);

    constructor(
        address _peggedToken,
        address _priceOracle,
        uint256 _mintThreshold,
        uint256 _burnThreshold
    ) {
        require(_peggedToken != address(0), "Invalid token address");
        require(_priceOracle != address(0), "Invalid price oracle address");
        require(_mintThreshold > 0, "Mint threshold must be greater than zero");
        require(_burnThreshold > 0, "Burn threshold must be greater than zero");

        peggedToken = IERC20(_peggedToken);
        priceOracle = _priceOracle;
        mintThreshold = _mintThreshold;
        burnThreshold = _burnThreshold;
    }

    /**
     * @dev Updates the price oracle address.
     * @param _priceOracle The new price oracle address.
     */
    function updatePriceOracle(address _priceOracle) external onlyOwner {
        require(_priceOracle != address(0), "Invalid price oracle address");
        priceOracle = _priceOracle;
    }

    /**
     * @dev Adjusts the supply of the pegged token based on the current price.
     */
    function adjustSupply() external {
        uint256 currentPrice = getCurrentPrice();

        if (currentPrice < mintThreshold) {
            // Mint new tokens if the price is below the mint threshold
            uint256 amountToMint = calculateMintAmount(currentPrice);
            require(amountToMint > 0, "Amount to mint must be greater than zero");
            // Assuming the peggedToken contract has a mint function
            _mintTokens(amountToMint);
        } else if (currentPrice > burnThreshold) {
            // Burn tokens if the price is above the burn threshold
            uint256 amountToBurn = calculateBurnAmount(currentPrice);
            require(amountToBurn > 0, "Amount to burn must be greater than zero");
            // Assuming the peggedToken contract has a burn function
            _burnTokens(amountToBurn);
        }
    }

    /**
     * @dev Internal function to mint tokens.
     * @param amount The amount of tokens to mint.
     */
    function _mintTokens(uint256 amount) internal {
        // Call the mint function of the pegged token
        // Ensure the peggedToken contract has a mint function
        (bool success, ) = address(peggedToken).call(abi.encodeWithSignature("mint(address,uint256)", address(this), amount));
        require(success, "Minting failed");
        emit TokensMinted(address(this), amount);
    }

    /**
     * @dev Internal function to burn tokens.
     * @param amount The amount of tokens to burn.
     */
    function _burnTokens(uint256 amount) internal {
        // Call the burn function of the pegged token
        // Ensure the peggedToken contract has a burn function
        (bool success, ) = address(peggedToken).call(abi.encodeWithSignature("burn(uint256)", amount));
        require(success, "Burning failed");
        emit TokensBurned(address(this), amount);
    }

    /**
     * @dev Retrieves the current price from the price oracle.
     * @return currentPrice The current price in wei.
     */
    function getCurrentPrice() internal view returns (uint256) {
        // This function should call the price oracle to get the current price
        // For demonstration purposes, we will return a mock price
        return 1 ether; // Replace with actual oracle call
    }

    /**
     * @dev Calculates the amount of tokens to mint based on the current price * @param currentPrice The current price in wei.
     * @return amountToMint The amount of tokens to mint.
     */
    function calculateMintAmount(uint256 currentPrice) internal view returns (uint256) {
        return (targetPrice.sub(currentPrice)).mul(1e18).div(targetPrice); // Example calculation
    }

    /**
     * @dev Calculates the amount of tokens to burn based on the current price.
     * @param currentPrice The current price in wei.
     * @return amountToBurn The amount of tokens to burn.
     */
    function calculateBurnAmount(uint256 currentPrice) internal view returns (uint256) {
        return (currentPrice.sub(targetPrice)).mul(1e18).div(targetPrice); // Example calculation
    }
}
