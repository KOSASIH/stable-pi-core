// stable-pi-core/api-gateway/adapters/polkadotAdapter.js

const { ApiPromise, WsProvider, Keyring, Decimal } = require('@polkadot/api');
const { cryptoWaitReady } = require('@polkadot/util-crypto');
require('dotenv').config();

const POLKADOT_API_URL = process.env.POLKADOT_API_URL || 'wss://rpc.polkadot.io'; // Set your Polkadot API URL in .env

// Initialize the Polkadot API
let api;

async function init() {
    await cryptoWaitReady();
    const provider = new WsProvider(POLKADOT_API_URL);
    api = await ApiPromise.create({ provider });
}

/**
 * Get the balance of a given Polkadot address.
 * @param {string} address - The Polkadot address to check.
 * @returns {Promise<string>} - The balance in DOT.
 */
async function getBalance(address) {
    try {
        const { data: { free: balance } } = await api.query.system.account(address);
        return Decimal(balance.toString()).div(1e10).toString(); // Convert from Plancks to DOT
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
        const transfer = api.tx.balances.transfer(toAddress, amount * 1e10); // Convert DOT to Plancks
        const hash = await transfer.signAndSend(sender);
        return hash.toHex(); // Return the transaction hash
    } catch (error) {
        throw new Error(`Failed to send DOT: ${error.message}`);
    }
}

/**
 * Monitor transaction status until confirmed.
 * @param {string} txHash - The transaction hash to monitor.
 * @returns {Promise<Object>} - The transaction status.
 */
async function monitorTransaction(txHash) {
    let confirmed = false;
    let attempts = 0;

    while (!confirmed && attempts < 10) {
        attempts++;
        const { status } = await api.rpc.chain.getBlock(txHash);
        if (status.isFinalized) {
            confirmed = true;
            return { txHash, status: 'confirmed' };
        }
        await new Promise(resolve => setTimeout(resolve, 5000)); // Wait for 5 seconds before checking again
    }

    throw new Error(`Transaction ${txHash} not confirmed after multiple attempts.`);
}

/**
 * Fetch transaction details by transaction hash.
 * @param {string} txHash - The transaction hash to fetch.
 * @returns {Promise<Object>} - The transaction details.
 */
async function getTransactionDetails(txHash) {
    try {
        const transaction = await api.rpc.chain.getBlock(txHash);
        return transaction; // Return the transaction details
    } catch (error) {
        throw new Error(`Failed to fetch transaction details: ${error.message}`);
    }
}

/**
 * Interact with a smart contract (Substrate-based).
 * @param {string} contractAddress - The address of the smart contract.
 * @param {Object} params - The parameters to pass to the contract.
 * @returns {Promise<string>} - The transaction hash.
 */
async function interactWithContract(contractAddress, params) {
    // Implement interaction logic with the smart contract
    // This is a placeholder; you will need to use a library or method to interact with the contract
    // Return the transaction hash
    return 'transaction_id_placeholder'; // Placeholder
}

// Initialize the adapter
init().catch(console.error);

// Export functions for use in other modules
module.exports = {
    getBalance,
    sendDOT,
    monitorTransaction,
    getTransactionDetails,
    interactWithContract,
};
