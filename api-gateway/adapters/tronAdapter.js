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
 * Monitor transaction status until confirmed.
 * @param {string} txID - The transaction ID to monitor.
 * @returns {Promise<Object>} - The transaction status.
 */
async function monitorTransaction(txID) {
    let confirmed = false;
    let attempts = 0;

    while (!confirmed && attempts < 10) {
        attempts++;
        const transaction = await tronWeb.trx.getTransaction(txID);
        if (transaction && transaction.ret[0].contractRet === 'SUCCESS') {
            confirmed = true;
            return { txID, status: 'confirmed' };
        }
        await new Promise(resolve => setTimeout(resolve, 5000)); // Wait for 5 seconds before checking again
    }

    throw new Error(`Transaction ${txID} not confirmed after multiple attempts.`);
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

/**
 * Interact with a smart contract on Tron.
 * @param {string} contractAddress - The address of the smart contract.
 * @param {string} methodName - The method to call on the contract.
 * @param {Array} params - The parameters to pass to the method.
 * @returns {Promise<string>} - The transaction ID.
 */
async function interactWithContract(contractAddress, methodName, params) {
    try {
        const contract = await tronWeb.contract().at(contractAddress);
        const tx = await contract[methodName](...params).send(); // Call the contract method
        return tx; // Return the transaction ID
    } catch (error) {
        throw new Error(`Failed to interact with contract: ${error.message}`);
    }
}

// Export functions for use in other modules
module.exports = {
    getBalance,
    sendTRX,
    monitorTransaction,
    getTransactionDetails,
    interactWithContract,
};
