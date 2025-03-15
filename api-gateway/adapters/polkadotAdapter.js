// stable-pi-core/api-gateway/adapters/polkadotAdapter.js

const { ApiPromise, WsProvider, Keyring } = require('@polkadot/api');
require('dotenv').config();

const POLKADOT_API_URL = process.env.POLKADOT_API_URL; // Set your Polkadot API URL in .env

// Initialize the Polkadot API
const provider = new WsProvider(POLKADOT_API_URL);
const api = await ApiPromise.create({ provider });

/**
 * Get the balance of a given Polkadot address.
 * @param {string} address - The Polkadot address to check.
 * @returns {Promise<string>} - The balance in DOT.
 */
async function getBalance(address) {
    try {
        const { data: { free: balance } } = await api.query.system.account(address);
        return balance.toString(); // Return balance in the smallest unit (Plancks)
    } catch (error) {
        throw new Error(`Failed to fetch balance: ${error.message}`);
    }
}

/**
 * Send DOT from one address to another.
 * @param {string} fromAddress - The sender's Polkadot address.
 * @param {string} toAddress - The recipient's Polkadot address.
 * @param {number} amount - The amount of DOT to send.
 * @param {string} senderPrivateKey - The sender's private key.
 * @returns {Promise<string>} - The transaction hash.
 */
async function sendDOT(fromAddress, toAddress, amount, senderPrivateKey) {
    const keyring = new Keyring({ type: 'sr25519' });
    const sender = keyring.addFromUri(senderPrivateKey);

    try {
        const transfer = api.tx.balances.transfer(toAddress, amount);
        const hash = await transfer.signAndSend(sender);
        return hash.toHex(); // Return the transaction hash
    } catch (error) {
        throw new Error(`Failed to send DOT: ${error.message}`);
    }
}

/**
 * Fetch transaction details by transaction hash.
 * @param {string} txHash - The transaction hash to fetch.
 * @returns {Promise<Object>} - The transaction details.
 */
async function getTransactionDetails(txHash) {
    try {
        const { status } = await api.rpc.chain.getBlock(txHash);
        return status; // Return the transaction status
    } catch (error) {
        throw new Error(`Failed to fetch transaction details: ${error.message}`);
    }
}

// Export functions for use in other modules
module.exports = {
    getBalance,
    sendDOT,
    getTransactionDetails,
};
