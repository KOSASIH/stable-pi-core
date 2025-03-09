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

/**
 * Validate that the email address is in a valid format.
 * @param {string} email - The email address to validate.
 * @throws Will throw an error if the email format is invalid.
 */
export const validateEmail = (email) => {
    const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    if (!emailRegex.test(email)) {
        throw new Error("Invalid email address format.");
    }
};

/**
 * Validate that the payment method is supported.
 * @param {string} method - The payment method to validate.
 * @throws Will throw an error if the payment method is unsupported.
 */
export const validatePaymentMethod = (method) => {
    const supportedMethods = ['coinbase', 'bitpay', 'on-chain'];
    if (!supportedMethods.includes(method)) {
        throw new Error(`Unsupported payment method: ${method}. Supported methods: ${supportedMethods.join(', ')}`);
    }
};
