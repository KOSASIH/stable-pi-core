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
 * Monitor transaction status until confirmed.
 * @param {string} txId - The transaction ID to monitor.
 * @returns {Promise<Object>} - The transaction status.
 */
async function monitorTransaction(txId) {
    let confirmed = false;
    let attempts = 0;

    while (!confirmed && attempts < 10) {
        attempts++;
        const transaction = await client.getTransaction(txId);
        if (transaction && transaction.confirmations > 0) {
            confirmed = true;
            return { txId, status: 'confirmed' };
        }
        await new Promise(resolve => setTimeout(resolve, 5000)); // Wait for 5 seconds before checking again
    }

    throw new Error(`Transaction ${txId} not confirmed after multiple attempts.`);
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

/**
 * Interact with a smart contract (if applicable).
 * @param {string} contractAddress - The address of the smart contract.
 * @param {Object} params - The parameters to pass to the contract.
 * @returns {Promise<string>} - The transaction ID.
 */
async function interactWithContract(contractAddress, params) {
    // Litecoin does not have traditional smart contracts like Ethereum,
    // but you can implement logic to interact with payment channels or other features.
    throw new Error('Smart contract interaction is not applicable for Litecoin.');
}

// Export functions for use in other modules
module.exports = {
    getBalance,
    sendLTC,
    monitorTransaction,
    getTransactionDetails,
    interactWithContract,
};
