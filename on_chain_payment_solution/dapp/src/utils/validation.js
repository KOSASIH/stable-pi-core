// utils/validation.js

/**
 * Validate that the amount is a positive number.
 * @param {number} amount - The amount to validate.
 * @throws Will throw an error if the amount is not a positive number.
 */
export const validateAmount = (amount) => {
    if (typeof amount !== 'number' || amount <= 0) {
        throw new Error("Amount must be a positive number.");
    }
};

/**
 * Validate that the currency is a valid ISO 4217 code.
 * @param {string} currency - The currency code to validate.
 * @throws Will throw an error if the currency code is invalid.
 */
export const validateCurrency = (currency) => {
    if (typeof currency !== 'string' || currency.length !== 3 || !/^[A-Z]+$/.test(currency)) {
        throw new Error("Currency must be a 3-letter ISO code.");
    }
};
