// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

contract MultiAssetCollateral is Ownable {
    using SafeMath for uint256;

    struct Collateral {
        address asset;
        uint256 amount;
    }

    struct UserPosition {
        Collateral[] collaterals;
        uint256 stablecoinMinted;
    }

    mapping(address => UserPosition) private userPositions;
    mapping(address => uint256) public assetPrices; // Mock price feed for assets
    uint256 public totalStablecoinMinted;

    event CollateralDeposited(address indexed user, address indexed asset, uint256 amount);
    event CollateralWithdrawn(address indexed user, address indexed asset, uint256 amount);
    event StablecoinMinted(address indexed user, uint256 amount);
    event StablecoinBurned(address indexed user, uint256 amount);

    // Set the price of an asset (for testing purposes)
    function setAssetPrice(address _asset, uint256 _price) external onlyOwner {
        assetPrices[_asset] = _price;
    }

    // Deposit collateral
    function depositCollateral(address _asset, uint256 _amount) external {
        require(_amount > 0, "Amount must be greater than zero");
        require(assetPrices[_asset] > 0, "Asset price not set");

        // Transfer asset to this contract
        IERC20(_asset).transferFrom(msg.sender, address(this), _amount);

        // Update user position
        UserPosition storage position = userPositions[msg.sender];
        position.collaterals.push(Collateral(_asset, _amount));

        emit CollateralDeposited(msg.sender, _asset, _amount);
    }

    // Withdraw collateral
    function withdrawCollateral(address _asset, uint256 _amount) external {
        UserPosition storage position = userPositions[msg.sender];
        uint256 totalCollateral = getTotalCollateralValue(msg.sender);

        require(totalCollateral >= _amount, "Insufficient collateral value");
        
        // Find and reduce the collateral amount
        for (uint256 i = 0; i < position.collaterals.length; i++) {
            if (position.collaterals[i].asset == _asset) {
                require(position.collaterals[i].amount >= _amount, "Insufficient collateral amount");
                position.collaterals[i].amount = position.collaterals[i].amount.sub(_amount);
                break;
            }
        }

        // Transfer asset back to user
        IERC20(_asset).transfer(msg.sender, _amount);
        emit CollateralWithdrawn(msg.sender, _asset, _amount);
    }

    // Mint stablecoin based on collateral value
    function mintStablecoin(uint256 _amount) external {
        UserPosition storage position = userPositions[msg.sender];
        uint256 totalCollateralValue = getTotalCollateralValue(msg.sender);

        require(totalCollateralValue >= _amount, "Insufficient collateral value to mint stablecoin");

        // Update user position
        position.stablecoinMinted = position.stablecoinMinted.add(_amount);
        totalStablecoinMinted = totalStablecoinMinted.add(_amount);

        emit StablecoinMinted(msg.sender, _amount);
    }

    // Burn stablecoin
    function burnStablecoin(uint256 _amount) external {
        UserPosition storage position = userPositions[msg.sender];
        require(position.stablecoinMinted >= _amount, "Insufficient stablecoin balance");

        // Update user position
        position.stablecoinMinted = position.stablecoinMinted.sub(_amount);
        totalStablecoinMinted = totalStablecoinMinted.sub(_amount);

        emit StablecoinBurned(msg.sender, _amount);
    }

    // Get total collateral value in stablecoin
    function getTotalCollateralValue(address user) public view returns (uint256 totalValue) {
        UserPosition storage position = userPositions[user];
        for (uint256 i = 0; i < position.collaterals.length; i++) {
            uint256 assetValue = position.collaterals[i].amount.mul(assetPrices[position.collaterals[i].asset]);
            totalValue = totalValue.add(assetValue);
        }
    }

    // Get user position details
    function getUserPosition(address user) external view returns (Collateral[] memory, uint256) {
        UserPosition storage position = userPositions[user];
        return (position.collaterals, position.stablecoinMinted);
    }
}
