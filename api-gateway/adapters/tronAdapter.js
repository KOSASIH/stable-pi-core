// stable-pi-core/api-gateway/adapters/tronAdapter.js

const TronWeb = require('tronweb');
require('dotenv').config();

const TRON_API_URL = process.env.TRON_API_URL || 'https://api.trongrid.io'; // Set your Tron API URL in .env

// Initialize TronWeb instance
const tronWeb = new TronWeb({
    fullHost: TRON_API_URL,
});

/**
 * Get the balance of a given Tron address.
 * @param {string} address - The Tron address to check.
 * @returns {Promise<number>} - The balance in TRX.
 */
async function getBalance(address) {
    try {
        const balance = await tronWeb.trx.getBalance(address);
        return balance / 1e6; // Convert SUN to TRX (1 TRX = 1,000,000 SUN)
    } catch (error) {
        throw new Error(`Failed to fetch balance: ${error.message}`);
    }
}

/**
 * Send TRX from one address to another.
 * @param {string} fromAddress - The sender's Tron address.
 * @param {string} toAddress - The recipient's Tron address.
 * @param {number} amount - The amount of TRX to send.
 * @param {string} senderPrivateKey - The sender's private key.
 * @returns {Promise<string>} - The transaction ID.
 */
async function sendTRX(fromAddress, toAddress, amount, senderPrivateKey) {
    try {
        // Set the private key for the sender
        tronWeb.setPrivateKey(senderPrivateKey);

        // Create and send the transaction
        const tx = await tronWeb.trx.sendTransaction(toAddress, amount * 1e6, fromAddress); // Convert TRX to SUN
        return tx.txid; // Return the transaction ID
    } catch (error) {
        throw new Error(`Failed to send TRX: ${error.message}`);
    }
}

/**
 * Fetch transaction details by transaction ID.
 * @param {string} txID - The transaction ID to fetch.
 * @returns {Promise<Object>} - The transaction details.
 */
async function getTransactionDetails(txID) {
    try {
        const transaction = await tronWeb.trx.getTransaction(txID);
        return transaction; // Return the transaction details
    } catch (error) {
        throw new Error(`Failed to fetch transaction details: ${error.message}`);
    }
}

// Export functions for use in other modules
module.exports = {
    getBalance,
    sendTRX,
    getTransactionDetails,
};
