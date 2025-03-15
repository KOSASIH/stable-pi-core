// stable-pi-core/api-gateway/adapters/tezosAdapter.js

const { TezosToolkit } = require('@taquito/taquito');
const { InMemorySigner } = require('@taquito/signer');
require('dotenv').config();

const TEZOS_API_URL = process.env.TEZOS_API_URL || 'https://mainnet.api.tez.ie'; // Set your Tezos API URL in .env

// Initialize the Tezos toolkit
const tezos = new TezosToolkit(TEZOS_API_URL);

/**
 * Get the balance of a given Tezos address.
 * @param {string} address - The Tezos address to check.
 * @returns {Promise<number>} - The balance in XTZ.
 */
async function getBalance(address) {
    try {
        const balance = await tezos.tz.getBalance(address);
        return balance.toNumber() / 1000000; // Convert mutez to XTZ
    } catch (error) {
        throw new Error(`Failed to fetch balance: ${error.message}`);
    }
}

/**
 * Send XTZ from one address to another.
 * @param {string} fromAddress - The sender's Tezos address.
 * @param {string} toAddress - The recipient's Tezos address.
 * @param {number} amount - The amount of XTZ to send.
 * @param {string} senderPrivateKey - The sender's private key.
 * @returns {Promise<string>} - The transaction hash.
 */
async function sendXTZ(fromAddress, toAddress, amount, senderPrivateKey) {
    try {
        // Set the signer
        tezos.setProvider({ signer: await InMemorySigner.fromSecretKey(senderPrivateKey) });

        // Create and send the transaction
        const operation = await tezos.tz.transfer({ to: toAddress, amount: amount });
        await operation.confirmation(); // Wait for confirmation

        return operation.hash; // Return the transaction hash
    } catch (error) {
        throw new Error(`Failed to send XTZ: ${error.message}`);
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
        const operation = await tezos.rpc.getOperation(txHash);
        if (operation && operation.status === 'applied') {
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
        const operation = await tezos.rpc.getOperation(txHash);
        return operation; // Return the transaction details
    } catch (error) {
        throw new Error(`Failed to fetch transaction details: ${error.message}`);
    }
}

/**
 * Interact with a smart contract (Michelson script).
 * @param {string} contractAddress - The address of the smart contract.
 * @param {Object} params - The parameters to pass to the contract.
 * @returns {Promise<string>} - The transaction hash.
 */
async function interactWithContract(contractAddress, params) {
    try {
        const contract = await tezos.contract.at(contractAddress);
        const operation = await contract.methods.someMethod(...params).send(); // Replace 'someMethod' with the actual method name
        await operation.confirmation(); // Wait for confirmation
        return operation.hash; // Return the transaction hash
    } catch (error) {
        throw new Error(`Failed to interact with contract: ${error.message}`);
    }
}

// Export functions for use in other modules
module.exports = {
    getBalance,
    sendXTZ,
    monitorTransaction,
    getTransactionDetails,
    interactWithContract,
};
