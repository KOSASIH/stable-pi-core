// stable-pi-core/api-gateway/adapters/cosmosAdapter.js

const { StargateClient, SigningStargateClient } = require('@cosmjs/stargate');
require('dotenv').config();

const COSMOS_API_URL = process.env.COSMOS_API_URL || 'https://rpc.cosmos.network'; // Set your Cosmos API URL in .env

// Initialize the Cosmos client
const client = await StargateClient.connect(COSMOS_API_URL);

/**
 * Get the balance of a given Cosmos address.
 * @param {string} address - The Cosmos address to check.
 * @returns {Promise<number>} - The balance in tokens.
 */
async function getBalance(address) {
    try {
        const balance = await client.getAllBalances(address);
        return balance; // Return balance in tokens
    } catch (error) {
        throw new Error(`Failed to fetch balance: ${error.message}`);
    }
}

/**
 * Send tokens from one address to another.
 * @param {string} fromAddress - The sender's Cosmos address.
 * @param {string} toAddress - The recipient's Cosmos address.
 * @param {number} amount - The amount of tokens to send.
 * @param {string} denom - The token denomination (e.g., 'uatom' for ATOM).
 * @param {string} senderPrivateKey - The sender's private key.
 * @returns {Promise<string>} - The transaction hash.
 */
async function sendTokens(fromAddress, toAddress, amount, denom, senderPrivateKey) {
    const wallet = await SigningStargateClient.connectWithSigner(COSMOS_API_URL, {
        mnemonic: senderPrivateKey, // Use mnemonic or private key
    });

    try {
        const fee = {
            amount: [{
                denom: denom,
                amount: '5000', // Fee amount in the same denomination
            }],
            gas: '200000', // Gas limit
        };

        const result = await wallet.sendTokens(fromAddress, toAddress, [{
            denom: denom,
            amount: amount.toString(),
        }], fee, 'Sending tokens');

        return result.transactionHash; // Return the transaction hash
    } catch (error) {
        throw new Error(`Failed to send tokens: ${error.message}`);
    }
}

/**
 * Fetch transaction details by transaction hash.
 * @param {string} txHash - The transaction hash to fetch.
 * @returns {Promise<Object>} - The transaction details.
 */
async function getTransactionDetails(txHash) {
    try {
        const transaction = await client.getTx(txHash);
        return transaction; // Return the transaction details
    } catch (error) {
        throw new Error(`Failed to fetch transaction details: ${error.message}`);
    }
}

// Export functions for use in other modules
module.exports = {
    getBalance,
    sendTokens,
    getTransactionDetails,
};
