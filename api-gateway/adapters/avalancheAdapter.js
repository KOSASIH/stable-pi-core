// stable-pi-core/api-gateway/adapters/avalancheAdapter.js

const { Avalanche, Buffer, BinTools, BufferReader, BufferWriter } = require('avalanche');
require('dotenv').config();

const AVALANCHE_API_URL = process.env.AVALANCHE_API_URL || 'https://api.avax.network'; // Set your Avalanche API URL in .env

// Initialize the Avalanche instance
const ava = new Avalanche(AVALANCHE_API_URL, 443, 'https');

// Get the AVM (Avalanche Virtual Machine) instance
const avm = ava.X; // AVM is used for asset management and transactions

/**
 * Get the balance of a given Avalanche address.
 * @param {string} address - The Avalanche address to check.
 * @returns {Promise<number>} - The balance in AVAX.
 */
async function getBalance(address) {
    try {
        const balance = await avm.getBalance(address);
        return balance.balance / 1e9; // Convert nAVAX to AVAX
    } catch (error) {
        throw new Error(`Failed to fetch balance: ${error.message}`);
    }
}

/**
 * Send AVAX from one address to another.
 * @param {string} fromAddress - The sender's Avalanche address.
 * @param {string} toAddress - The recipient's Avalanche address.
 * @param {number} amount - The amount of AVAX to send.
 * @param {string} senderPrivateKey - The sender's private key.
 * @returns {Promise<string>} - The transaction ID.
 */
async function sendAVAX(fromAddress, toAddress, amount, senderPrivateKey) {
    try {
        const keyPair = avm.keyChain.getKey(senderPrivateKey);
        const tx = await avm.buildTx({
            from: fromAddress,
            to: toAddress,
            amount: amount * 1e9, // Convert AVAX to nAVAX
        });

        // Sign the transaction
        const signedTx = keyPair.signTx(tx);

        // Send the transaction
        const txID = await avm.sendTx(signedTx);
        return txID; // Return the transaction ID
    } catch (error) {
        throw new Error(`Failed to send AVAX: ${error.message}`);
    }
}

/**
 * Fetch transaction details by transaction ID.
 * @param {string} txID - The transaction ID to fetch.
 * @returns {Promise<Object>} - The transaction details.
 */
async function getTransactionDetails(txID) {
    try {
        const tx = await avm.getTx(txID);
        return tx; // Return the transaction details
    } catch (error) {
        throw new Error(`Failed to fetch transaction details: ${error.message}`);
    }
}

// Export functions for use in other modules
module.exports = {
    getBalance,
    sendAVAX,
    getTransactionDetails,
};
