const Web3 = require('web3');

/**
 * Validates if a given string is a valid Ethereum address.
 * @param {string} address - The Ethereum address to validate.
 * @returns {boolean} - Returns true if valid, false otherwise.
 */
function isValidEthereumAddress(address) {
    return Web3.utils.isAddress(address);
}

/**
 * Formats a number to a fixed decimal point.
 * @param {number} number - The number to format.
 * @param {number} decimals - The number of decimal places.
 * @returns {string} - The formatted number as a string.
 */
function formatNumber(number, decimals = 2) {
    return Number(number).toFixed(decimals);
}

/**
 * Generates a random string of specified length.
 * @param {number} length - The length of the random string.
 * @returns {string} - The generated random string.
 */
function generateRandomString(length) {
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    let result = '';
    for (let i = 0; i < length; i++) {
        result += characters.charAt(Math.floor(Math.random() * characters.length));
    }
    return result;
}

/**
 * Calculates the fee based on a percentage of the total amount.
 * @param {number} amount - The total amount.
 * @param {number} feePercentage - The fee percentage to calculate.
 * @returns {number} - The calculated fee.
 */
function calculateFee(amount, feePercentage) {
    return (amount * feePercentage) / 100;
}

/**
 * Logs an error message to the console.
 * @param {string} message - The error message to log.
 */
function logError(message) {
    console.error(`[ERROR] ${new Date().toISOString()}: ${message}`);
}

/**
 * Logs an info message to the console.
 * @param {string} message - The info message to log.
 */
function logInfo(message) {
    console.log(`[INFO] ${new Date().toISOString()}: ${message}`);
}

module.exports = {
    isValidEthereumAddress,
    formatNumber,
    generateRandomString,
    calculateFee,
    logError,
    logInfo,
};
