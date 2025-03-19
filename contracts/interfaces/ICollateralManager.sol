// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title ICollateralManager
 * @dev Interface for managing collateral in a DeFi protocol.
 */
interface ICollateralManager {
    
    /**
     * @dev Emitted when collateral is deposited.
     * @param user The address of the user depositing collateral.
     * @param asset The address of the asset being deposited.
     * @param amount The amount of collateral deposited.
     */
    event CollateralDeposited(address indexed user, address indexed asset, uint256 amount);

    /**
     * @dev Emitted when collateral is withdrawn.
     * @param user The address of the user withdrawing collateral.
     * @param asset The address of the asset being withdrawn.
     * @param amount The amount of collateral withdrawn.
     */
    event CollateralWithdrawn(address indexed user, address indexed asset, uint256 amount);

    /**
     * @dev Emitted when collateral is liquidated.
     * @param user The address of the user whose collateral is being liquidated.
     * @param asset The address of the asset being liquidated.
     * @param amount The amount of collateral liquidated.
     */
    event CollateralLiquidated(address indexed user, address indexed asset, uint256 amount);

    /**
     * @dev Deposit collateral into the system.
     * @param asset The address of the asset to deposit.
     * @param amount The amount of collateral to deposit.
     */
    function depositCollateral(address asset, uint256 amount) external;

    /**
     * @dev Withdraw collateral from the system.
     * @param asset The address of the asset to withdraw.
     * @param amount The amount of collateral to withdraw.
     */
    function withdrawCollateral(address asset, uint256 amount) external;

    /**
     * @dev Check the collateral balance of a user.
     * @param user The address of the user.
     * @param asset The address of the asset to check.
     * @return The amount of collateral held by the user for the specified asset.
     */
    function getCollateralBalance(address user, address asset) external view returns (uint256);

    /**
     * @dev Check if a user is over-collateralized.
     * @param user The address of the user to check.
     * @return True if the user is over-collateralized, false otherwise.
     */
    function isOverCollateralized(address user) external view returns (bool);

    /**
     * @dev Liquidate a user's collateral if they are under-collateralized.
     * @param user The address of the user to liquidate.
     * @param asset The address of the asset to liquidate.
     * @param amount The amount of collateral to liquidate.
     */
    function liquidateCollateral(address user, address asset, uint256 amount) external;

    /**
     * @dev Get the total collateral value of a user in the system.
     * @param user The address of the user.
     * @return The total value of collateral held by the user.
     */
    function getTotalCollateralValue(address user) external view returns (uint256);
}
