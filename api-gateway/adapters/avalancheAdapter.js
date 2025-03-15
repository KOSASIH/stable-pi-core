// stable-pi-core/api-gateway/adapters/avalancheAdapter.js

const { Avalanche, Buffer, BinTools, BufferReader, BufferWriter, KeyChain } = require('avalanche');
require('dotenv').config();

const AVALANCHE_API_URL = process.env.AVALANCHE_API_URL || 'https://api.avax.network'; // Set your Avalanche API URL in .env

// Initialize the Avalanche instance
const ava = new Avalanche(AVALANCHE_API_URL, 443, 'https');
const avm = ava.X; // AVM is used for asset management and transactions
const keyChain = avm.keyChain();

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
        const keyPair = keyChain.getKey(senderPrivateKey);
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
 * Monitor transaction status until confirmed.
 * @param {string} txID - The transaction ID to monitor.
 * @returns {Promise<Object>} - The transaction status.
 */
async function monitorTransaction(txID) {
    let confirmed = false;
    let attempts = 0;

    while (!confirmed && attempts < 10) {
        attempts++;
        const status = await avm.getTxStatus(txID);
        if (status && status.status === 'accepted') {
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
        const tx = await avm.getTx(txID);
        return tx; // Return the transaction details
    } catch (error) {
        throw new Error(`Failed to fetch transaction details: ${error.message}`);
    }
}

/**
 * Interact with a smart contract on Avalanche.
 * @param {string} contractAddress - The address of the smart contract.
 * @param {Array} params - The parameters to pass to the contract.
 * @returns {Promise<string>} - The transaction ID.
 */
async function interactWithContract(contractAddress, params) {
    // Implement interaction logic with the smart contract
    // This is a placeholder; you will need to use a library or method to interact with the contract
    // Return the transaction ID
    return 'transaction_id_placeholder'; // Placeholder
}

// Export functions for use in other modules
module.exports = {
    getBalance,
    sendAVAX,
    monitorTransaction,
    getTransactionDetails,
    interactWithContract,
};
