// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IAutomatedContract {
    /**
     * @dev Emitted when an automated action is executed.
     * @param actionId The unique identifier for the action.
     * @param executor The address that executed the action.
     * @param success A boolean indicating whether the action was executed successfully.
     * @param result The result of the action execution, if applicable.
     */
    event ActionExecuted(
        uint256 indexed actionId,
        address indexed executor,
        bool success,
        bytes result
    );

    /**
     * @dev Emitted when an action's parameters are updated.
     * @param actionId The unique identifier for the action.
     * @param params The new parameters for the action.
     */
    event ActionParametersUpdated(uint256 indexed actionId, bytes params);

    /**
     * @dev Executes an automated action based on the provided parameters.
     * @param actionId The unique identifier for the action to be executed.
     * @param params The parameters required for executing the action.
     * @return success A boolean indicating whether the action was executed successfully.
     * @return result The result of the action execution, if applicable.
     */
    function executeAction(uint256 actionId, bytes calldata params) external returns (bool success, bytes memory result);

    /**
     * @dev Gets the status of a specific action.
     * @param actionId The unique identifier for the action.
     * @return executed A boolean indicating whether the action has been executed.
     * @return success A boolean indicating whether the last execution was successful.
     * @return result The result of the last action execution, if applicable.
     */
    function getActionStatus(uint256 actionId) external view returns (bool executed, bool success, bytes memory result);

    /**
     * @dev Sets the parameters for a specific action.
     * @param actionId The unique identifier for the action.
     * @param params The parameters to be set for the action.
     */
    function setActionParameters(uint256 actionId, bytes calldata params) external;

    /**
     * @dev Gets the parameters for a specific action.
     * @param actionId The unique identifier for the action.
     * @return params The parameters associated with the action.
     */
    function getActionParameters(uint256 actionId) external view returns (bytes memory params);

    /**
     * @dev Checks if an action is executable based on its current state and parameters.
     * @param actionId The unique identifier for the action.
     * @return executable A boolean indicating whether the action can be executed.
     */
    function isActionExecutable(uint256 actionId) external view returns (bool executable);
}
