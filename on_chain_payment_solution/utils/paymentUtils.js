// utils/paymentUtils.js

/**
 * Format the amount for display or API requests.
 * @param {number} amount - The amount to format.
 * @param {string} currency - The currency code.
 * @returns {string} - The formatted amount.
 */
export const formatAmount = (amount, currency) => {
    if (currency === "USD") {
        return `$${amount.toFixed(2)}`;
    } else {
        return `${amount.toFixed(2)} ${currency}`;
    }
};

/**
 * Calculate the total amount from a list of items.
 * @param {Array} items - The list of items, each with a price and quantity.
 * @returns {number} - The total amount.
 */
export const calculateTotalAmount = (items) => {
    return items.reduce((total, item) => {
        return total + (item.price * item.quantity);
    }, 0);
};

/**
 * Generate a unique order ID.
 * @returns {string} - A unique order ID.
 */
export const generateOrderId = () => {
    return `ORDER-${Date.now()}-${Math.floor(Math.random() * 10000)}`;
};
