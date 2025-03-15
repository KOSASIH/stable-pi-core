// stable-pi-core/api-gateway/adapters/litecoinAdapter.js

const Litecoin = require('litecoin');
require('dotenv').config();

const LTC_API_URL = process.env.LTC_API_URL || 'http://localhost:9332'; // Set your Litecoin API URL in .env

// Initialize the Litecoin client
const client = new Litecoin.Client({
    host: LTC_API_URL,
    username: process.env.LTC_RPC_USER, // Set your Litecoin RPC username in .env
    password: process.env.LTC_RPC_PASSWORD, // Set your Litecoin RPC password in .env
});

/**
 * Get the balance of a given Litecoin address.
 * @param {string} address - The Litecoin address to check.
 * @returns {Promise<number>} - The balance in LTC.
 */
async function getBalance(address) {
    try {
        const balance = await client.getAddressBalance(address);
        return balance; // Return balance in LTC
    } catch (error) {
        throw new Error(`Failed to fetch balance: ${error.message}`);
    }
}

/**
 * Send LTC from one address to another.
 * @param {string} fromAddress - The sender's Litecoin address.
 * @param {string} toAddress - The recipient's Litecoin address.
 * @param {number} amount - The amount of LTC to send.
 * @param {string} senderPrivateKey - The sender's private key.
 * @returns {Promise<string>} - The transaction ID.
 */
async function sendLTC(fromAddress, toAddress, amount, senderPrivateKey) {
    try {
        // Create a transaction
        const tx = await client.createTransaction({
            from: fromAddress,
            to: toAddress,
            amount: amount,
            privateKey: senderPrivateKey,
        });

        // Send the transaction
        const txId = await client.sendTransaction(tx);
        return txId; // Return the transaction ID
    } catch (error) {
        throw new Error(`Failed to send LTC: ${error.message}`);
    }
}

/**
 * Fetch transaction details by transaction ID.
 * @param {string} txId - The transaction ID to fetch.
 * @returns {Promise<Object>} - The transaction details.
 */
async function getTransactionDetails(txId) {
    try {
        const transaction = await client.getTransaction(txId);
        return transaction; // Return the transaction details
    } catch (error) {
        throw new Error(`Failed to fetch transaction details: ${error.message}`);
    }
}

// Export functions for use in other modules
module.exports = {
    getBalance,
    sendLTC,
    getTransactionDetails,
};
