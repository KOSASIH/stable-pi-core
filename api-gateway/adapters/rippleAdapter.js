// stable-pi-core/api-gateway/adapters/rippleAdapter.js

const ripple = require('ripple-lib');
require('dotenv').config();

const XRP_API_URL = process.env.XRP_API_URL || 'wss://s1.ripple.com'; // Set your Ripple API URL in .env

// Initialize the Ripple API client
const api = new ripple.RippleAPI({ server: XRP_API_URL });

/**
 * Get the balance of a given Ripple address.
 * @param {string} address - The Ripple address to check.
 * @returns {Promise<number>} - The balance in XRP.
 */
async function getBalance(address) {
    try {
        const accountInfo = await api.getAccountInfo(address);
        return accountInfo.xrpBalance; // Return balance in XRP
    } catch (error) {
        throw new Error(`Failed to fetch balance: ${error.message}`);
    }
}

/**
 * Send XRP from one address to another.
 * @param {string} fromAddress - The sender's Ripple address.
 * @param {string} toAddress - The recipient's Ripple address.
 * @param {number} amount - The amount of XRP to send.
 * @param {string} senderSecret - The sender's secret key.
 * @returns {Promise<string>} - The transaction hash.
 */
async function sendXRP(fromAddress, toAddress, amount, senderSecret) {
    try {
        // Prepare the transaction
        const preparedTx = await api.preparePayment(fromAddress, {
            source: {
                address: fromAddress,
                maxAmount: {
                    value: amount.toString(),
                    currency: 'XRP'
                }
            },
            destination: {
                address: toAddress,
                amount: {
                    value: amount.toString(),
                    currency: 'XRP'
                }
            }
        });

        // Sign the transaction
        const signedTx = api.sign(preparedTx.txJSON, senderSecret);

        // Submit the transaction
        const result = await api.submit(signedTx.signedTransaction);
        return result.tx_json.hash; // Return the transaction hash
    } catch (error) {
        throw new Error(`Failed to send XRP: ${error.message}`);
    }
}

/**
 * Fetch transaction details by transaction hash.
 * @param {string} txHash - The transaction hash to fetch.
 * @returns {Promise<Object>} - The transaction details.
 */
async function getTransactionDetails(txHash) {
    try {
        const transaction = await api.getTransaction(txHash);
        return transaction; // Return the transaction details
    } catch (error) {
        throw new Error(`Failed to fetch transaction details: ${error.message}`);
    }
}

// Export functions for use in other modules
module.exports = {
    getBalance,
    sendXRP,
    getTransactionDetails,
};
