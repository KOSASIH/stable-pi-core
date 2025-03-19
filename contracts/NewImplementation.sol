// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract NewImplementation {
    // State variable to store a value
    uint256 private value;

    // Event to log value changes
    event ValueChanged(uint256 newValue);
    event ValueReset();

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
        emit ValueReset();
    }

    // New feature: Multiply the current value by a given factor
    function multiplyValue(uint256 factor) external {
        require(factor > 0, "Factor must be greater than zero");
        value *= factor;
        emit ValueChanged(value);
    }

    // New feature: Divide the current value by a given divisor
    function divideValue(uint256 divisor) external {
        require(divisor > 0, "Divisor must be greater than zero");
        value /= divisor;
        emit ValueChanged(value);
    }

    // New feature: Get the square of the current value
    function squareValue() external {
        value = value * value;
        emit ValueChanged(value);
    }
}
