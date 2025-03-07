// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract MultiAssetReserve is Ownable {
    // State variables
    mapping(address => uint256) public reserves; // Mapping of asset addresses to their reserves
    mapping(address => bool) public isAssetSupported; // Mapping to check if an asset is supported
    address[] public supportedAssets; // List of supported assets

    // Events
    event ReserveUpdated(address indexed asset, uint256 amount);
    event AssetSupported(address indexed asset);
    event AssetUnsupported(address indexed asset);
    event EmergencyWithdrawal(address indexed asset, uint256 amount);

    // Function to support a new asset
    function supportAsset(address asset) public onlyOwner {
        require(asset != address(0), "Invalid asset address");
        require(!isAssetSupported[asset], "Asset already supported");
        
        isAssetSupported[asset] = true; // Mark the asset as supported
        supportedAssets.push(asset); // Add to the list of supported assets
        emit AssetSupported(asset);
    }

    // Function to remove support for an asset
    function removeAssetSupport(address asset) public onlyOwner {
        require(isAssetSupported[asset], "Asset not supported");
        
        isAssetSupported[asset] = false; // Mark the asset as unsupported
        emit AssetUnsupported(asset);
    }

    // Function to update reserves for a specific asset
    function updateReserve(address asset, uint256 amount) public onlyOwner {
        require(isAssetSupported[asset], "Asset not supported");
        require(amount > 0, "Amount must be greater than zero");
        
        reserves[asset] += amount; // Update the reserve for the specified asset
        emit ReserveUpdated(asset, reserves[asset]);
    }

    // Function to withdraw assets in case of emergency
    function emergencyWithdraw(address asset, uint256 amount) public onlyOwner {
        require(isAssetSupported[asset], "Asset not supported");
        require(reserves[asset] >= amount, "Insufficient reserve");
        
        reserves[asset] -= amount; // Decrease the reserve
        IERC20(asset).transfer(owner(), amount); // Transfer the asset to the owner
        emit EmergencyWithdrawal(asset, amount);
    }

    // Function to get the reserve amount for a specific asset
    function getReserve(address asset) public view returns (uint256) {
        return reserves[asset];
    }

    // Function to calculate total reserve value (example implementation)
    function calculateTotalReserveValue(address priceFeed) public view returns (uint256 totalValue) {
        // This function would require external price feeds to calculate the total value of reserves
        // For simplicity, we will return a placeholder value
        totalValue = 0;
        for (uint256 i = 0; i < supportedAssets.length; i++) {
            address asset = supportedAssets[i];
            uint256 reserveAmount = reserves[asset];
            uint256 assetPrice = getAssetPrice(asset, priceFeed); // Fetch the price from the price feed
            totalValue += reserveAmount * assetPrice; // Calculate total value
        }
    }

    // Placeholder function to get asset price from an external price feed
    function getAssetPrice(address asset, address priceFeed) internal view returns (uint256) {
        // Implement logic to fetch price from the price feed
        // This is a placeholder; actual implementation will depend on the price feed used
        return 1; // Placeholder value
    }
}
