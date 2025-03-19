// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

library SafeMath {
    /**
     * @dev Returns the addition of two unsigned integers, reverting on
     * overflow.
     */
    function add(uint256 a, uint256 b) internal pure returns (uint256) {
        uint256 c = a + b;
        require(c >= a, "SafeMath: addition overflow");

        return c;
    }

    /**
     * @dev Returns the subtraction of two unsigned integers, reverting on
     * underflow (when the result is negative).
     */
    function sub(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b <= a, "SafeMath: subtraction underflow");
        uint256 c = a - b;

        return c;
    }

    /**
     * @dev Returns the multiplication of two unsigned integers, reverting on
     * overflow.
     */
    function mul(uint256 a, uint256 b) internal pure returns (uint256) {
        if (a == 0) {
            return 0;
        }
        uint256 c = a * b;
        require(c / a == b, "SafeMath: multiplication overflow");

        return c;
    }

    /**
     * @dev Returns the integer division of two unsigned integers. Reverts on
     * division by zero. The result is rounded towards zero.
     */
    function div(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b > 0, "SafeMath: division by zero");
        uint256 c = a / b;

        return c;
    }

    /**
     * @dev Returns the remainder of dividing two unsigned integers. (unsigned
     * integer modulo), reverting when dividing by zero.
     */
    function mod(uint256 a, uint256 b) internal pure returns (uint256) {
        require(b > 0, "SafeMath: modulo by zero");
        return a % b;
    }

    // Signed integer operations

    /**
     * @dev Returns the addition of two signed integers, reverting on
     * overflow.
     */
    function add(int256 a, int256 b) internal pure returns (int256) {
        int256 c = a + b;
        require((b > 0 && c > a) || (b < 0 && c < a), "SafeMath: addition overflow");

        return c;
    }

    /**
     * @dev Returns the subtraction of two signed integers, reverting on
     * underflow (when the result is negative).
     */
    function sub(int256 a, int256 b) internal pure returns (int256) {
        int256 c = a - b;
        require((b > 0 && c > a) || (b < 0 && c < a), "SafeMath: subtraction underflow");

        return c;
    }

    /**
     * @dev Returns the multiplication of two signed integers, reverting on
     * overflow.
     */
    function mul(int256 a, int256 b) internal pure returns (int256) {
        if (a == 0) {
            return 0;
        }
        int256 c = a * b;
        require(c / a == b, "SafeMath: multiplication overflow");

        return c;
    }

    /**
     * @dev Returns the integer division of two signed integers. Reverts on
     * division by zero. The result is rounded towards zero.
     */
    function div(int256 a, int256 b) internal pure returns (int256) {
        require(b != 0, "SafeMath: division by zero");
        require(!(a == type(int256).min && b == -1), "SafeMath: division overflow");
        return a / b;
    }

    /**
     * @dev Returns the remainder of dividing two signed integers. (signed
     * integer modulo), reverting when dividing by zero.
     */
    function mod(int256 a, int256 b) internal pure returns (int256) {
        require(b != 0, "SafeMath: modulo by zero");
        return a % b;
    }
}
