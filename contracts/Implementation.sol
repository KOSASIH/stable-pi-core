// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Implementation {
    // State variable to store a value
    uint256 private value;

    // Event to log value changes
    event ValueChanged(uint256 newValue);

    // Function to set a new value
    function setValue(uint256 _value) external {
        value = _value;
        emit ValueChanged(_value);
    }

    // Function to get the current value
    function getValue() external view returns (uint256) {
        return value;
    }

    // Function to increment the current value
    function incrementValue() external {
        value += 1;
        emit ValueChanged(value);
    }

    // Function to decrement the current value
    function decrementValue() external {
        require(value > 0, "Value cannot be negative");
        value -= 1;
        emit ValueChanged(value);
    }

    // Function to reset the value to zero
    function resetValue() external {
        value = 0;
        emit ValueChanged(value);
    }
}
